def filter_to_multiple_votes(votes_df, min_usr_votes=4, min_post_votes=4):
    ''' filter the list of votes to one in which both users and posts have a minimum number of votes'''
    
    old_length = None

    votes_df = votes_df.copy()
    
    while old_length != len(votes_df):
        old_length = len(votes_df)

        # get votes that have been made by users who have made multiple votes
        usr_votes_multi = set()
        for grp in votes_df.groupby('USERNAME'):
            username = grp[0]
            if len(grp[1]) >= min_usr_votes:
                usr_votes_multi.add(username)
        votes_df = votes_df[votes_df['USERNAME'].isin(usr_votes_multi)]
        
        # get the IDs of submissions that have multiple votes
        pol_votes_multi_ids = set()
        for grp in votes_df.groupby('SUBMISSION_ID'):
            if len(grp[1]) >= min_post_votes:
                pol_votes_multi_ids.add(grp[0])
        votes_df = votes_df[votes_df['SUBMISSION_ID'].isin(pol_votes_multi_ids)]
    return(votes_df)

def print_most_changed(sample, submissions_df):
    ''' Print the titles of posts with the greatest change between the Neeka algorithm and simple-consensus '''
    neeka_promoted = sample.sort_values(by='DIFFERENCE_RANK', ascending=False)
    simple_promoted = neeka_promoted[::-1]
    
    print("Most Promoted by **Neeka Consensus** over simple-consensus (most demoted by simple-consensus):")
    for i, post in enumerate(neeka_promoted[:10].itertuples(), start=1):
        title = submissions_df.loc[post.Index]['TITLE']
        print(f'{i}. "{title}"')
    
    print('-')
    
    print("Most Promoted by **simple-consensus** over Neeka (most demoted by Neeka):")
    for i, post in enumerate(simple_promoted[:10].itertuples(), start=1):
        title = submissions_df.loc[post.Index]['TITLE']
        print(f'{i}. "{title}"')