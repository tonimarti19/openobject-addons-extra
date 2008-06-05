##############################################################################
#
# Copyright (c) 2004 TINY SPRL. (http://tiny.be) All Rights Reserved.
#					Fabien Pinckaers <fp@tiny.Be>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from osv import osv, fields

VoteValues = [('0','Very Bad'),('25', 'Bad'),('50','None'),('75','Good'),('100','Very Good') ]
DefaultVoteValue = '50'
MaximumVoteValue = '100'

class idea_category(osv.osv):
	_name = "idea.category"
	_description = "Category for an idea"
	_columns = {
		'name': fields.char('Category', size=64, required=True),
		'summary' : fields.char('Summary', size=255 ),
	}
	_sql_constraints = [
		('name', 'unique(name)', 'The name of the category must be unique' )
	]
	_order = 'name asc'

idea_category()

class idea_idea(osv.osv):
	_name = 'idea.idea'
	_rec_name = 'title'

	def _vote_avg_compute(self, cr, uid, ids, name, arg, context = None):
		if not len(ids):
			return {}

		sql = """select i.id, avg(v.score::integer) 
				   from idea_idea i left outer join idea_vote v on i.id = v.idea_id
					where i.id in (%s)
					group by i.id
				""" % ','.join(['%d']*len(ids))

		cr.execute(sql, ids)
		return dict(cr.fetchall())

	def _vote_count(self,cr,uid,ids,name,arg,context=None):
		if not len(ids):
			return {}

		sql = """select i.id, count(1) 
				   from idea_idea i left outer join idea_vote v on i.id = v.idea_id
					where i.id in (%s)
					group by i.id
				""" % ','.join(['%d']*len(ids))

		cr.execute(sql, ids)
		return dict(cr.fetchall())

	def _comment_count(self,cr,uid,ids,name,arg,context=None):
		if not len(ids):
			return {}

		sql = """select i.id, count(1) 
				   from idea_idea i left outer join idea_comment c on i.id = c.idea_id
					where i.id in (%s)
					group by i.id
				""" % ','.join(['%d']*len(ids))


		cr.execute(sql,ids)
		return dict(cr.fetchall())

	def _vote_read(self, cr, uid, ids, name, arg, context = None):
		res = {}
		vote_obj = self.pool.get('idea.vote')
		votes_ids = vote_obj.search(cr, uid, [('idea_id', 'in', ids), ('user_id', '=', uid)])
		for vote in vote_obj.browse(cr, uid, votes_ids, context):
			res[vote.idea_id.id] = vote.score

		return res

	def _vote_save(self, cr, uid, id, field_name, field_value, arg, context = None):
		vote_obj = self.pool.get('idea.vote')
		vote = vote_obj.search(cr,uid,[('idea_id', '=', id),('user_id', '=', uid)])
		textual_value = str(field_value)
		if vote:
			vote_obj.write(cr,uid, vote[0], { 'score' : textual_value })
		else:
			vote_obj.create(cr,uid, { 'idea_id' : id, 'user_id' : uid, 'score' : textual_value })


	_columns = {
		'user_id': fields.many2one('res.users', 'Creator', required=True, readonly=True),
		'title': fields.char('Idea Summary', size=64, required=True),
		'description': fields.text('Description', required=True, help='Content of the idea'),
		'comment_ids': fields.one2many('idea.comment', 'idea_id', 'Comments'),
		'create_date' : fields.datetime( 'Creation date', readonly=True),
		'vote_ids' : fields.one2many('idea.vote', 'idea_id', 'Vote'),
		'my_vote' : fields.function(_vote_read, fnct_inv = _vote_save, string="My Vote", method=True, type="selection", selection=VoteValues),
		'vote_avg' : fields.function(_vote_avg_compute, method=True, string="Average Score", type="float"),
		'count_votes' : fields.function(_vote_count, method=True, string="Count of votes", type="integer"),
		'count_comments': fields.function(_comment_count, method=True, string="Count of comments", type="integer"),
		'category_id': fields.many2one('idea.category', 'Category', required=True ),
		'state': fields.selection([('draft','Draft'),('open','Opened'),('close','Closed'),('cancel','Canceled')], 'State', readonly=True),

		'stat_vote_ids': fields.one2many('idea.vote.stat', 'idea_id', 'Statistics', readonly=True),
	}

	_defaults = {
		'user_id': lambda self,cr,uid,context: uid,
		'my_vote': lambda *a: MaximumVoteValue, 
		'state': lambda *a: 'draft'
	}

	_order = 'id desc'


	def idea_cancel(self, cr, uid, ids):
		self.write(cr, uid, ids, { 'state' : 'cancel' })
		return True

	def idea_open(self, cr, uid, ids):
		self.write(cr, uid, ids, { 'state' : 'open' })
		return True

	def idea_close(self, cr, uid, ids):
		self.write(cr, uid, ids, { 'state' : 'close' })
		return True

	def idea_draft(self, cr, uid, ids):
		self.write(cr, uid, ids, { 'state' : 'draft' })
		return True


idea_idea()

class idea_comment(osv.osv):
	_name = 'idea.comment'
	_description = 'Comments'
	_rec_name = 'content'
	_columns = {
		'idea_id': fields.many2one('idea.idea', 'Idea', required=True, ondelete='cascade' ),
		'user_id': fields.many2one('res.users', 'User', required=True ),
		'content': fields.text( 'Comment', required=True ),
		'create_date' : fields.datetime( 'Creation date', readonly=True),
	}
	_defaults = {
		'user_id': lambda self, cr, uid, context: uid
	}
	_order = 'id desc'

idea_comment()

class idea_vote(osv.osv):
	_name = 'idea.vote'
	_rec_name = 'score'
	_columns = {
		'user_id': fields.many2one( 'res.users', 'User'),
		'idea_id': fields.many2one('idea.idea', 'Idea', required=True, ondelete='cascade'),
		'score': fields.selection( VoteValues, 'Score', required=True)
	}
	_defaults = {
		'score': lambda *a: DefaultVoteValue,
	}

idea_vote()


class idea_vote_stat(osv.osv):
	_name = 'idea.vote.stat'
	_description = 'Idea Votes Statistics'
	_auto = False
	_rec_name = 'idea_id'
	_columns = {
		'idea_id': fields.many2one('idea.idea', 'Idea', readonly=True),
		'score': fields.selection( VoteValues, 'Score', readonly=True),
		'nbr': fields.integer('Number of Votes', readonly=True),
	}
	def init(self, cr):
		"""
		initialize the sql view for the stats
		
		cr -- the cursor
		"""
		cr.execute("""
			create or replace view idea_vote_stat as (
				select
					min(v.id) as id,
					i.id as idea_id,
					v.score,
					count(1) as nbr
				from
					idea_vote v
					left join 
					idea_idea i on (v.idea_id=i.id)
				group by
					i.id, v.score, i.id
		)""")
	
idea_vote_stat()
