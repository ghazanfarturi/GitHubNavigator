import os.path
import cherrypy
import requests
import json
import collections
from datetime import datetime


# Algorithm GitHubNavigator
#	Input: GitHub repositories and their latest commits data that contain search_term.
#	Output: Populate the template.html with data required in the template file.
#
#	send HttpRequest using GET to GitHub Api for all the repsitories
#	If search_term is not conatin in HttpResponse return null
#	repository_dictionary <-- ListOfValues[repository_name, created_at, owner_url, owner_avator_url, owner_login]
#	
#	foreach repository_name in ListOfValues, do
#		send HttpRequest using GET to GitHib Api for each repository master branch
#		repository_dictionary <-- ListOfValues[sha, commit_message, commit_author_name]
#	return repository_dictionary


# Design Pattern: ModelViewPresenter (MVP)
# No usage of AntiPattern such as "Tunneling everything through GET". As in this exercise we are only interested to read data of
# specific parameters that means we are only we are only retrieving a resource using GET method. 


class GitHubNavigator(object):
	# Index page
	@cherrypy.expose
	def index(self):
		return 'Please type your desired search term in the address as: hostaddress/navigator?search_term=YOUR_DESIRE_SEARCH_TERM'

	# Navigator page
	@cherrypy.expose
	def navigator(self, search_term):
		# Algorithm Implementation here:
		# Create HTTP Session
		session = requests.Session()
		# Create reponse object and send http request to Github API
		response = session.get('https://api.github.com/search/repositories?q=topic:' + search_term + '&page=1&per_page=5&sort=created_at&order=desc')
		# Create JSON object from response returned from http request
		json_data = json.loads(response.text)
		
		# Declare variable for Navigation Dictionary and Repositories List here so that there scope is visible to the nested level
		navigation_dict = {}
		sorted_dict = {}
		repo_list = []
		# Checks for successful call and also the search_term exist in GitHub repositories
		if (response.status_code == 200) and (json_data['total_count'] > 0):
			# Loop through json_data and assign all the required elements to navigation_dict
			for repo in json_data['items']:
				# Create a repository list which will be required to get the latest commits from each individual repository
				repo_list.append((repo['name'], repo['full_name']))
				navigation_dict[repo['name']] = {
					"full_name": repo['full_name'],
					"created_at": datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
					"owner_url": repo['owner']['url'],
					"owner_avatar_url": repo['owner']['avatar_url'],
					"owner_login": repo['owner']['login']
				}
				
			# We got the repository list now its time to navigate to each individual repository in order to get the lastest commit
			j = 0
			for i in repo_list:
				response = session.get('https://api.github.com/repos/' + repo_list[j][1] + '/commits/master')
				json_data = json.loads(response.text)
				if 'sha' not in json_data:
					return 'GitHub API Calls maximum Limit reached, please wait for 30 minutes'
				else: 
					# Append the sha, commit_message and commit_author_name to navigation_dict
					navigation_dict[i[0]]['sha'] = json_data['sha']
					navigation_dict[i[0]]['commit_message'] = json_data['commit']['message']
					navigation_dict[i[0]]['commit_author_name'] = json_data['commit']['author']['name']
				j += 1	
			# Create a sorted response dictionary so that the latest created repositories are shown on top 
			sorted_dict = collections.OrderedDict(sorted(navigation_dict.items(), key=lambda item: item[1]['created_at'], reverse=True ))
		else:
			return 'sorry your desired word is not found in any of the GitHut repository please try something different'
		
		return { 'repositories' : sorted_dict.items(), 'search_term' : search_term }
	
	@cherrypy.expose		
	def test(self):
		repo_dict ={'Android-ExpandIcon': {'commit_author_name': 'Zagumennyi Evgenii',
					'commit_message': 'Update README.md',
					'created_at': '2016-12-26T10:10:03Z',
					'full_name': 'zagum/Android-ExpandIcon',
					'owner_avatar_url': 'https://avatars3.githubusercontent.com/u/2884888?v=4',
					'owner_login': 'zagum',
					'owner_url': 'https://api.github.com/users/zagum',
					'sha': '62ec783f6bf35e34661ddea78df68701620aff91'},
			'Arrow': {'commit_author_name': 'S4cha',
					'commit_message': 'Swift 4.1 and Xcode 9.3 support - v4.1.0',
					'created_at': '2015-06-07T12:42:50Z',
					'full_name': 'freshOS/Arrow',
					'owner_avatar_url': 'https://avatars0.githubusercontent.com/u/20884428?v=4',
					'owner_login': 'freshOS',
					'owner_url': 'https://api.github.com/users/freshOS',
					'sha': '9f9ef355a1509c0a9effa8b1dbfadb4af2ea865f'},
			'SexyTooltip': {'commit_author_name': 'Tyler Sheaffer',
					'commit_message': 'download link is releases',
					'created_at': '2014-11-15T18:59:46Z',
					'full_name': 'calm/SexyTooltip',
					'owner_avatar_url': 'https://avatars1.githubusercontent.com/u/5170572?v=4',
					'owner_login': 'calm',
					'owner_url': 'https://api.github.com/users/calm',
					'sha': 'f84a0bcfa096b551bec8002407f5ccd898fcf928'},
			'actual-number-picker': {'commit_author_name': 'Milos Marinkovic',
					'commit_message': 'Updating demo project to use the latest version',
					'created_at': '2015-08-15T18:10:55Z',
					'full_name': 'milosmns/actual-number-picker',
					'owner_avatar_url': 'https://avatars3.githubusercontent.com/u/1771914?v=4',
					'owner_login': 'milosmns',
					'owner_url': 'https://api.github.com/users/milosmns',
					'sha': '03a4fbf49fa5ab5cce9b70783e3047dbb84a23a9'},
			'leader-line': {'commit_author_name': 'anseki',
					'commit_message': 'Add pkg.scripts.test',
					'created_at': '2016-10-24T05:48:56Z',
					'full_name': 'anseki/leader-line',
					'owner_avatar_url': 'https://avatars2.githubusercontent.com/u/4763469?v=4',
					'owner_login': 'anseki',
					'owner_url': 'https://api.github.com/users/anseki',
					'sha': '9dc757ce7adb25bbd18eda02fe023af22a915943'}}
		import collections
		sd = collections.OrderedDict(sorted(repo_dict.items()))
		return { 'repositories': sd.items(), 'search_term': 'arrow' }


if __name__ == '__main__':
	# Boilerplate code copied from cherrypy documentation
	# Register the Mako plugin
	from mako_templating.makoplugin import MakoTemplatePlugin
	MakoTemplatePlugin(cherrypy.engine, base_dir=os.getcwd()).subscribe()

	# Boilerplate code copied from cherrypy documentation
	# Register the Mako tool
	from mako_templating.makotool import MakoTool
	cherrypy.tools.template = MakoTool()

	# Boilerplate code copied from cherrypy documentation
	# We must disable the encode tool because it
	# transforms our dictionary into a list which
	# won't be consumed by the mako tool
	cherrypy.quickstart(GitHubNavigator(), '', {'/': {'tools.template.on': True,
							  'tools.template.template': 'template.html',
							  'tools.encode.on': False}})
