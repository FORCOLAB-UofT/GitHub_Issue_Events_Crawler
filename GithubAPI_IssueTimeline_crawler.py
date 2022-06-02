import stscraper as scraper
import pandas as pd
import json
import os,time


class repoMethod(scraper.GitHubAPI):
    
    @scraper.api_filter(lambda issue: 'pull_request' not in issue)
    @scraper.api('repos/%s/issues', paginate=True, state='closed')
    def repo_closed_issues(self, repo_slug):
        """Get repository issues (not including pull requests)"""
        # https://developer.github.com/v3/issues/#list-issues-for-a-repository
        return repo_slug

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
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': "",
                    'created_at': event.get('created_at'),
                    'id': event['source']['issue']['number'],
                    'repo': event['source']['issue']['repository']['full_name'],
                    'type': 'pull_request' if 'pull_request' in event['source']['issue'].keys() else 'issue',
                    'state': event['source']['issue']['state'],
                    'assignees': event['source']['issue']['assignees'],
                    'label': "",
                    'body': ''
                }
            elif event['event'] == 'referenced':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'labeled':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'label': event['label']['name'],
                    'body': ''
                }
            elif event['event'] == 'unlabeled':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'label': event['label']['name'],
                    'body': ''
                }
            elif event['event'] == 'committed':
                yield {
                    'event': event['event'],
                    'author': event['author']['name'],
                    'email': event['author']['email'],
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
                    'body': ''
                }
            elif event['event'] == 'reviewed':
                author = event['user'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'commented':
                yield {
                    'event': event['event'],
                    'author': event['user']['login'],
                    'email': '',
                    'author_type': event['user']['type'],
                    'author_association': event['author_association'],
                    'commit_id': '',
                    'created_at': event.get('created_at'),
                    'id': '',
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': event['body']
                }
            elif event['event'] == 'assigned':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'unassigned':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'closed':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'subscribed':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': event['commit_id'],
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': ''
                }
            elif event['event'] == 'unsubscribed':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': event['commit_id'],
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': ''
                }
            elif event['event'] == 'merged':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
                    'email': '',
                    'author_type': author.get('type'),
                    'author_association': '',
                    'commit_id': event['commit_id'],
                    'created_at': event.get('created_at'),
                    'id': event['commit_id'],
                    'repo': '',
                    'type': '',
                    'state': '',
                    'assignees': '',
                    'label': '',
                    'body': ''
                }
            elif event['event'] == 'mentioned':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'connected':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'disconnected':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'milestoned':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'label': event['milestone']['title'],
                    'body': ''
                }
            elif event['event'] == 'demilestoned':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'label': event['milestone']['title'],
                    'body': ''
                }
            elif event['event'] == 'marked_as_duplicate':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'unmarked_as_duplicate':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'locked':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'unlocked':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'convert_to_draft':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'ready_for_review':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'pinned':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'unpinned':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'reopened':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'renamed':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'label': event['rename'].get('from'),
                    'body': event['rename'].get('to')
                }
            elif event['event'] == 'transferred':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'body': ''
                }
            elif event['event'] == 'review_requested':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'requester': event['review_requester'].get('login'),
                    'reviewer': event['requested_reviewer'].get('login')
                }
            elif event['event'] == 'review_requested_removed':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'requester': event['review_requester'].get('login'),
                    'reviewer': event['requested_reviewer'].get('login')
                }
            elif event['event'] == 'review_dismissed':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                    'dismissed_state': event['dismissed_review'].get('state'),
                    'dismissal_message': event['dismissed_review'].get('dismissal_message')
                }
            elif event['event'] == 'head_ref_restored':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                }
            elif event['event'] == 'head_ref_force_pushed':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                }
            elif event['event'] == 'head_ref_deleted':
                author = event['actor'] or {}
                yield {
                    'event': event['event'],
                    'author': author.get('login'),
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
                }                
            else:
                yield {
                    'event': event['event'],
                    'author': '',
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
                    'body': ''
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

def get_timeline_repo(pull_df,filepath,reposlug):
    indexOverall=0
    currentrepo_timeline_dfs=[]

    for i in range(pull_df.shape[0]):
        start_time=time.time()
        print(indexOverall)
        current_issue_number=pull_df.iloc[i]['number']

        current_timeline=gh_api.issue_pr_timeline(reposlug,int(current_issue_number))
        timeline_df=pd.DataFrame(current_timeline)
        timeline_df["repo_source"]=reposlug
        timeline_df["issue_number"]=current_issue_number
        timeline_df["issue_type"]="pulls"
        timeline_df["issue_status"]="closed"
        currentrepo_timeline_dfs.append(timeline_df)
        indexOverall+=1
        end_time=time.time()
        times=round(end_time-start_time,2)
        print('total scraping time is{}s'.format(times))
        print(indexOverall)

    mergeddf=pd.concat(currentrepo_timeline_dfs,ignore_index=True)
    return mergeddf



#main 
if __name__ == '__main__':

    savefilepath=" "

    # Your github tokens for using GithubAPI
    gh_api =repoMethod("token1,token2,token3,token4,token5")


    # the list of repo slugs that you want to collected timeline events of issues for.
    
    repo_list=read_keywords_list('file path')

    for i in range(len(repo_list)):
        result_obj=gh_api.repo_pullrequests(example_repo[i],"closed")
        if i == 0:
            PRs_df=pd.DataFrame(result_obj)
            event_df=get_timeline_repo(PRs_df,example_repo[i])
        elif i > 0:
            More_PRs_df=pd.DataFrame(result_obj)
            More_event_df=get_timeline_repo(More_PRs_df,example_repo[i])
            event_df=event_df.append(More_event_df)

    event_df.to_excel(savefilepath+"events_file.xls")


