import stscraper as scraper
import pandas as pd
import json
import os,time
import mysql.connector
import mySettings
from datetime import datetime
from stscraper import base
import requests

class repoMethod(scraper.GitHubAPI):
    
    @scraper.api_filter(lambda issue: 'pull_request' not in issue)
    @scraper.api('repos/%s/issues', paginate=True, state='closed')
    def repo_closed_issues(self, repo_slug):
        """Get repository issues (not including pull requests)"""
        # https://developer.github.com/v3/issues/#list-issues-for-a-repository
        return repo_slug

    def repo_all_pr_issues(self, repo_slug):
        """return the result of pull requests"""
        #https://developer.github.com/v3/pulls/#list-pull-requests
        url ='repos/'+repo_slug+'/issues'
        repo_pr_issues= self.request(url, paginate=True,state="all")
        return repo_pr_issues


    def repo_pullrequests(self, repo_slug,pull_state):
        """return the result of pull requests"""
        #https://developer.github.com/v3/pulls/#list-pull-requests
        url ='repos/'+repo_slug+'/pulls'
        repopulls= self.request(url, paginate=True,state=pull_state)
        return repopulls

    def repo_contributor_count(self, repo_slug):
        """return the result of contributor"""
        url ='repos/'+repo_slug+'/contributors'
        repocontr= self.request(url, paginate=True)
        return repocontr
    
    def repo_commits_count(self, repo_slug):
        url ='repos/'+repo_slug+'/commits'
        repocomts= self.request(url, paginate=True)
        return repocomts
    
    def repo_api_check(self, repo_slug):
        url='repos/'+repo_slug
        repoResponse=self.request(url,paginate=False)
        return repoResponse

    def search_closed_issues(self, repo_source_slug, repo_mentioned_slug):
        """ Return timeline on an issue or a pull request
                :param repo: str 'owner/repo'url
                :param issue_id: int, either an issue or a Pull Request id
                """
        # append to repos['items'] list
        # keep going through the results pages and extract ['items']
        # append extracted items to original
        q=repo_mentioned_slug+'+type:issues+state:closed+repo:'+repo_source_slug
        url = 'search/issues?q='+q
        repos = self.request(url, paginate=False)
        page = 1
        total_repos = min(repos['total_count'], 1000)
        items_remaining = total_repos - len(repos['items'])
        while items_remaining > 0:
            print("Repository search results remaining: {}".format(items_remaining))
            # next page
            page += 1
            url ='search/issues?q='+q+'&page='+str(page)
            repos['items'] += self.request(url, paginate=False)['items']
            items_remaining = total_repos - len(repos['items'])
        return repos



    #from https://github.com/shuiblue/GitHubAPI-Crawler by Prof.Shurui Zhou, for collecting issue/PR timelines
    def issue_pr_timeline(self, repo, issue_id):
        """ Return timeline on an issue or a pull request
        :param repo: str 'owner/repo'url
        :param issue_id: int, either an issue or a Pull Request id
        """
        url = "repos/%s/issues/%s/timeline" % (repo, issue_id)
        events = self.request(url, paginate=True, state='all')
        for event in events:
            # print('repo: ' + repo + ' issue: ' + str(issue_id) + ' event: ' + event['event'])
            if event['event'] == 'cross-referenced':
                author = event['actor'] or {}
                assignees = event['source']['issue']['assignees'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': "",
                    'created_at': event.get('created_at'),
                    'id': event['source']['issue']['number'],
                    'repo': event['source']['issue']['repository']['full_name'],
                    'type': 'pull_request' if 'pull_request' in event['source']['issue'].keys() else 'issue',
                    'state': event['source']['issue']['state'],
                    'assignees': ''.join(assignee.get('login') for assignee in assignees),
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'referenced':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event['created_at'],
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'labeled':
                author = event['actor'] or {}
                label = event['label'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': label['name'],
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'unlabeled':
                author = event['actor'] or {}
                label = event['label'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': label['name'],
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'committed':
                author = event['author'] or {}
                yield {
                    'event': event['event'],
                    'author': '',
                    'author_name': author['name'],
                    'email': author['email'],
                    'author_type': '',
                    'author_association': '',
                    'commit_id': event['sha'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'reviewed':
                author = event['user'] or {}
                html_link = event['_links']['html'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': event['author_association'],
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': event['state'],
                    'assignees': '',
                    'label': '',
                    'body': event['body'],
                    'submitted_at': event.get('submitted_at'),
                    'links': html_link.get('href'),
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'commented':
                user = event['user']
                yield {
                    'event': event['event'],
                    'author': user['login'],
                    'author_name': '',
                    'email': '',
                    'author_type': user['type'],
                    'author_association': event['author_association'],
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': event['body'],
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'assigned':
                author = event['actor'] or {}
                assignees = event['assignee'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': assignees.get('login'),
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'unassigned':
                author = event['actor'] or {}
                assignees = event['assignee'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': assignees.get('login'),
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'closed':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'subscribed':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'unsubscribed':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'merged':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'mentioned':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'connected':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': '',
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'disconnected':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': '',
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'milestoned':
                author = event['actor'] or {}
                milestone = event['milestone'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': milestone['title'],
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'demilestoned':
                author = event['actor'] or {}
                milestone = event['milestone'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': milestone['title'],
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'marked_as_duplicate':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'unmarked_as_duplicate':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'locked':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': event['lock_reason'],
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'unlocked':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'convert_to_draft':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label':'',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'ready_for_review':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'pinned':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label':'',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'unpinned':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'reopened':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'renamed':
                author = event['actor'] or {}
                rename = event['rename'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': rename.get('from'),
                    'body': rename.get('to'),
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'transferred':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'review_requested':
                author = event['actor'] or {}
                requester = event['review_requester'] or {}
                try:
                    reviewer = event['requested_reviewer']['login'] or{} 
                except:
                    reviewer = event['requested_team']['name'] or{} 
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': requester.get('login'),
                    'reviewer': reviewer,
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'review_requested_removed':
                author = event['actor'] or {}
                requester = event['review_requester'] or {}
                try:
                    reviewer = event['requested_reviewer']['login'] or{} 
                except:
                    reviewer = event['requested_team']['name'] or{} 
                
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': requester.get('login'),
                    'reviewer': reviewer,
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'review_dismissed':
                author = event['actor'] or {}
                review = event['dismissed_review'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': review.get('state'),
                    'dismissal_message': review.get('dismissal_message')
                }
            elif event['event'] == 'head_ref_restored':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'head_ref_force_pushed':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'head_ref_deleted':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'author_name': '',
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'commit-commented':
                comments = event['comments'] or {}
                users = []
                for comment in comments:
                    if comment['user'] != None:
                        users.append(comment['user'])
                    else:
                        users.append({})
                yield {
                    'event': event['event'],
                    'author': ', '.join(str(user.get('login') or '') for user in users),
                    'author_name': '',
                    'email': '',
                    'author_type': ', '.join(str(user.get('type') or '') for user in users),
                    'author_association': ', '.join(comment['author_association'] for comment in comments),
                    'commit_id': ', '.join(comment['commit_id'] for comment in comments),
                    'created_at': ', '.join(comment.get('created_at') for comment in comments),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': ''.join(comment['body'] for comment in comments),
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }
            elif event['event'] == 'line-commented':
                comments = event['comments'] or {}
                users = []
                for comment in comments:
                    if comment['user'] != None:
                        users.append(comment['user'])
                    else:
                        users.append({})
                yield {
                    'event': event['event'],
                    'author': ', '.join(str(user.get('login') or '') for user in users),
                    'author_name': '',
                    'email': '',
                    'author_type': ', '.join(str(user.get('type') or '') for user in users),
                    'author_association': ', '.join(comment['author_association'] for comment in comments),
                    'commit_id': ', '.join(comment['commit_id'] for comment in comments),
                    'created_at': ', '.join(comment.get('created_at') for comment in comments),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': ''.join(comment['body'] for comment in comments),
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }            
            else:
                yield {
                    'event': event['event'],
                    'author': '',
                    'author_name': '',
                    'email': '',
                    'author_type': '',
                    'author_association': '',
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': '',
                    'submitted_at': '',
                    'links': '',
                    'old_name': '',
                    'new_name': '',
                    'requester': '',
                    'reviewer': '',
                    'dismissed_state': '',
                    'dismissal_message': ''
                }



def read_json_df(filename):
    jsonfile=open(filename,encoding="utf-8")
    obj=jsonfile.read()
    commitsJson=json.loads(obj)
    jsondf=pd.DataFrame(commitsJson)
    jsonfile.close()

    return jsondf

def read_excel_df(filename):
    df = pd.read_excel(filename,sheet_name=0)
    df=pd.DataFrame(df)
    return df


def read_keywords_list(path):
    with open(path) as wordfile:
        keywords_list = wordfile.read().splitlines()
    wordfile.close()

    return keywords_list



def get_timeline_repo_pr(issue_num,issue_type,issue_status, reposlug, repo_index):

    start_time=time.time()

    print(str(reposlug) + ' PR/issue #'+ str(issue_num) + '\n')
    f.write(str(reposlug) + ' PR/issue #'+ str(issue_num) + '\n')

    try:
        current_timeline=gh_api.issue_pr_timeline(reposlug,int(issue_num))
        timeline_df=pd.DataFrame(current_timeline)
        timeline_df["repo_id"]=repo_index
        timeline_df["repo_source"]=reposlug
        timeline_df["issue_number"]=issue_num
        timeline_df["issue_type"]=issue_type
        timeline_df["issue_status"]=issue_status
        
        insert=("INSERT INTO `timeline_events`.`issue_pr_event`"
                "(`event`, `author`, `author_name`, `email`, `author_type`,"
                "`author_association`, `commit_id`, `created_at`, `id`, `repo`, "
                "`type`, `state`,`assignees`, `label`, `body`, "
                "`submitted_at`, `links`, `old_name`, `new_name`, `requester`, "
                "`reviewer`, `dismissed_state`, `dismissal_message`, `repo_id`, `repo_source`, "
                "`issue_number`, `issue_type`, `issue_status`) VALUES"
                "(%s,%s,%s,%s,%s,"
                "%s,%s,%s,%s,%s,"
                "%s,%s,%s,%s,%s,"
                "%s,%s,%s,%s,%s,"
                "%s,%s,%s,%s,%s,"
                "%s,%s,%s);")        
        
        mycursor.executemany(insert, timeline_df.values.tolist())
        mydb.commit()
        end_time=time.time()
        times=round(end_time-start_time,2)
        print('PR/issue #'+ str(issue_num) + ' query successfully')
        f.write('PR/issue #' + str(issue_num) + ' query successfully \n')
        print('total scraping time is {}s'.format(times) + '\n')
        f.write('total scraping time is {}s'.format(times) + '\n\n')
    # except base.RepoDoesNotExist:
    #     print ("repo "+str(reposlug) + " does not exist \n")
    #     f.write ("repo "+str(reposlug) + " does not exist \n")
    except requests.Timeout:
        print("timeout exception")
        f.write("requesting API timeout for "+str(reposlug) + ' PR/issue #'+ str(issue_num) + '\n')





#main 
if __name__ == '__main__':



    # server connection
    #import mySettings, detailed creditials for connections and github tokens are listed in mySettings.py under the same directory as this file
    mydb = mySettings.db

    mycursor = mydb.cursor(buffered=True)

    print("connected to database")
    # Your github tokens for using GithubAPI
    gh_api =repoMethod(mySettings.tokens)

    ### repo_list table from database, disabled for now July 5th, 2022,
    ### since current goal is to collect the first 623 repos that have more than 500 prs and the complete repo
    ### list has more repos than desired
    # mycursor.execute('SELECT count(*) FROM repo_list;')
    # len_repo_list = int(mycursor.fetchone()[0])
    len_repo_list=623

    ### @jy set the limit to 624 to collect first 623 repos
    mycursor.execute('SELECT * FROM repo_list order by repo_index asc limit 624;')
    repo_list = mycursor.fetchall()
    
    f = open("/data/timeline_events/GitHub_Issue_Events_Crawler/log/events_crawler_log_2.txt", "a")

    
    for i in range(len_repo_list):
        example_repo = repo_list[i][1]
        repo_index = repo_list[i][0]

        mycursor.execute('SELECT 1 FROM scraped_repos where repo_index= %s limit 1;',(repo_index,))
        b_repo_scraped = len(mycursor.fetchall())
        if b_repo_scraped:
            f.write('repo :' + str(example_repo) + ' has been scraped \n')
            continue
        else:
            mycursor.execute('SELECT 1 FROM issue_pr_event where repo_id= %s limit 1;',(repo_index,))
            repo_exist = len(mycursor.fetchall())
            f.write('scraping repo :' + str(example_repo) + ' now  \n')

            if repo_exist:
                print("repo "+str(example_repo)+" exists in pr_issue_event list, now checking pr/issue number of the repo")
                f.write("repo "+str(example_repo)+" exists in pr_issue_event list, now checking pr/issue number of the repo \n")
                try:
                    # print("repo exist , getting all issues line 1314")
                    repo_pr_issues=gh_api.repo_all_pr_issues(example_repo)
                    # print("repo exist , got all issues line 1316")
                    for item in repo_pr_issues:
                        # print("collecting issue loop begins")
                        issue_id=item['number']
                        issue_or_pr='pull' if 'pull_request' in item else 'issue'
                        created_at=item['created_at']
                        updated_at=item['updated_at']
                        closed_at=item['closed_at']
                        author_login=item['user']['login']
                        issue_status=item['state']

                        mycursor.execute('SELECT 1 FROM pr_issue where repo_index= %s and issue_id=%s limit 1;',(repo_index,issue_id))
                        pr_exist = len(mycursor.fetchall())
                        if pr_exist:
                            today=datetime.now()
                            f.write(str(today)+": repo "+str(example_repo)+" issue "+str(issue_id)+" already exist \n")        
                            continue
                        else:
                            # get timeline for current issue
                            try: 
                                # print(" pr doesnt exist, getting timeline, line 1344")
                                get_timeline_repo_pr(issue_id,issue_or_pr,issue_status,example_repo,repo_index)
                                print(" pr doesnt exist, finished getting timeline, line 1346")
                                today=datetime.now()
                                print(str(today)+": repo "+str(example_repo)+" issue "+str(issue_id)+" timeline events querying done, now writing to database \n")
                                f.write(str(today)+": repo "+str(example_repo)+" issue "+str(issue_id)+" timeline events querying done, now writing to database \n")                                                            

                                sql = "INSERT INTO pr_issue (repo_index, issue_id, issue_or_pr, created_at,updated_at, closed_at, author_login, issue_status) VALUES (%s, %s, %s, %s,%s,%s,%s,%s)"
                                val = (repo_index,issue_id,issue_or_pr,created_at,updated_at,closed_at,author_login,issue_status)
                                mycursor.execute(sql, val)
                                mydb.commit()
                                print(str(today)+": repo "+str(example_repo)+" issue "+str(issue_id)+" timeline events querying done, writing to database done \n")
                                f.write(str(today)+": repo "+str(example_repo)+" issue "+str(issue_id)+" timeline events querying done, writing to database done \n")                                                            

                            except:
                                today=datetime.now()
                                print(str(today)+": repo "+str(example_repo)+" issue "+str(issue_id)+" timeline events querying failed \n")
                                f.write(str(today)+": repo "+str(example_repo)+" issue "+str(issue_id)+" timeline events querying failed \n")                                                            

                except base.RepoDoesNotExist:
                    print ("repo "+str(example_repo) + " does not exist \n")
                    f.write ("repo "+str(example_repo) + " does not exist \n")
                # except:
                #     f.write("repo "+str(example_repo)+" pr issue do not exist \n")
            else:
                try:
                    repo_pr_issues=gh_api.repo_all_pr_issues(example_repo)
                    # print("repo doesnt exist , got all issues line 1358")
                    for item in repo_pr_issues:
                        issue_id=item['number']
                        issue_or_pr='pull' if 'pull_request' in item else 'issue'
                        created_at=item['created_at']
                        updated_at=item['updated_at']
                        closed_at=item['closed_at']
                        author_login=item['user']['login']
                        issue_status=item['state']
                        sql = "INSERT INTO pr_issue (repo_index, issue_id, issue_or_pr, created_at,updated_at, closed_at, author_login, issue_status) VALUES (%s, %s, %s, %s,%s,%s,%s,%s)"

                        val = (repo_index,issue_id,issue_or_pr,created_at,updated_at,closed_at,author_login,issue_status)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        

                        get_timeline_repo_pr(issue_id,issue_or_pr,issue_status,example_repo,repo_index)
                        # print("got timeline line 1378")
                except base.RepoDoesNotExist:
                    print ("repo "+str(example_repo) + " does not exist \n")
                    f.write ("repo "+str(example_repo) + " does not exist \n")


            mycursor.execute('SELECT count(issue_id) FROM timeline_events.pr_issue where repo_index =%s',(repo_index,))
            pr_issues_count = int(mycursor.fetchone()[0])

            # finished collecting all pr/issue & timelines for this repo, add the repo name into the scraped_repos table.
            sql = "INSERT INTO scraped_repos (`repo_index`,`pr_issues_count`,`repo_name`,`scraped_at`) VALUES (%s, %s, %s, %s)"
            now_timestp=str(datetime.utcnow())

            val = (repo_index,pr_issues_count,example_repo,now_timestp)
            mycursor.execute(sql, val)
            mydb.commit()

    f.close()
