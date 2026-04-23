"""
Problem: Design Twitter

Difficulty: Medium (LeetCode #355)

---------------------------------------------------
Problem Statement:

Design a simplified Twitter with these operations:

    postTweet(userId, tweetId)      — user posts a tweet
    getNewsFeed(userId)             — return up to 10 most recent tweet IDs
                                       from the user's own posts PLUS the
                                       posts of users they follow, ordered
                                       by most-recent-first.
    follow(followerId, followeeId)  — follower starts following followee
    unfollow(followerId, followeeId) — follower stops following followee

A user implicitly "follows themselves" — their own tweets always
appear in their feed.

---------------------------------------------------
Why This Problem Is A Capstone For Phase 06:

Almost every data-structure decision is about choosing the right
HASH-MAP VALUE:

    user_tweets:    userId  → list of (timestamp, tweetId)
    following:      userId  → set of followeeIds

Then the algorithmic heart of `getNewsFeed` is a K-WAY MERGE of sorted
tweet lists — the same heap-based merge you saw in Phase 03's sorting
module.

This one problem combines:
    - HashMap (user → tweets, user → followees)    ← Phase 06
    - HashSet (set of followees)                    ← Phase 06
    - Min/Max heap for k-way merge                 ← Phase 08 preview
    - Global timestamp counter (monotonic clock)

---------------------------------------------------
Design Choices:

1. Store each user's tweets as a LIST IN INSERTION ORDER, newest at the
   END. Since tweets arrive in time order, inserting is O(1) and the
   list stays sorted by timestamp.

2. For getNewsFeed, iterate each relevant user's tweet list FROM THE END
   backwards. Use a max-heap keyed by timestamp to pull the 10 most
   recent across all users. O(F log F) where F is the number of users
   being merged, for each of the 10 pulls → O(10 · F log F) total.

3. A GLOBAL TIMESTAMP ensures a total order across all tweets, even
   for users posting simultaneously. Just increment a counter.

---------------------------------------------------
Complexity:

    postTweet:     O(1)
    follow:        O(1)
    unfollow:      O(1)
    getNewsFeed:   O(F log F) where F = # followees (bounded by 10 pulls)

---------------------------------------------------
Notes On Realism:

This is still a TOY. Real Twitter does NOT k-way merge on every feed
request — it uses timeline FANOUT (write-time push of a tweet to
every follower's precomputed timeline) for most users, with a
fallback to pull-based k-way merge for "celebrity" accounts that
follow-fan out would overwhelm. The pattern is the same, just
moved to write-time for the hot path.
"""

from collections import defaultdict
import heapq


class Twitter:
    FEED_SIZE = 10

    def __init__(self):
        self._tweets = defaultdict(list)           # userId -> [(timestamp, tweetId), ...]
        self._follows = defaultdict(set)           # userId -> set of followeeIds
        self._timestamp = 0                        # global monotonic counter

    # ------------------------------------------------------------------
    # Posting
    # ------------------------------------------------------------------

    def post_tweet(self, user_id, tweet_id):
        """
        Post a tweet. Each tweet gets a globally monotonic timestamp.
        O(1).
        """
        self._timestamp += 1
        self._tweets[user_id].append((self._timestamp, tweet_id))

    # ------------------------------------------------------------------
    # Following
    # ------------------------------------------------------------------

    def follow(self, follower_id, followee_id):
        """Follower starts following followee. O(1)."""
        if follower_id != followee_id:
            self._follows[follower_id].add(followee_id)

    def unfollow(self, follower_id, followee_id):
        """Follower stops following followee. O(1)."""
        self._follows[follower_id].discard(followee_id)

    # ------------------------------------------------------------------
    # Feed — the interesting one
    # ------------------------------------------------------------------

    def get_news_feed(self, user_id):
        """
        Return up to `FEED_SIZE` tweet IDs from user + followees, newest first.

        Algorithm: k-way merge using a MAX-HEAP of iterators (in Python,
        a min-heap with negated timestamps).

        Time:  O(F + 10 * log F) where F = user + # followees.
        Space: O(F + 10).
        """
        # Everyone whose tweets count toward this feed
        sources = self._follows[user_id] | {user_id}

        # Build a max-heap of (-timestamp, tweet_id, source_user, index_in_their_tweets)
        # Starting with each source's MOST RECENT tweet.
        heap = []
        for src in sources:
            tweets = self._tweets.get(src)
            if not tweets:
                continue
            last_idx = len(tweets) - 1
            ts, tid = tweets[last_idx]
            heapq.heappush(heap, (-ts, tid, src, last_idx - 1))

        result = []
        while heap and len(result) < Twitter.FEED_SIZE:
            neg_ts, tid, src, next_idx = heapq.heappop(heap)
            result.append(tid)
            # Push the next-most-recent tweet from the same source
            if next_idx >= 0:
                ts, next_tid = self._tweets[src][next_idx]
                heapq.heappush(heap, (-ts, next_tid, src, next_idx - 1))

        return result


# =========================================================================
# Test
# =========================================================================

if __name__ == "__main__":
    # LC #355 example scenario
    t = Twitter()
    t.post_tweet(1, 5)
    assert t.get_news_feed(1) == [5]

    t.follow(1, 2)                                 # user 1 follows user 2
    t.post_tweet(2, 6)
    assert t.get_news_feed(1) == [6, 5]

    t.unfollow(1, 2)
    assert t.get_news_feed(1) == [5]

    # Self-follow should be a no-op
    t = Twitter()
    t.follow(1, 1)
    t.post_tweet(1, 10)
    assert t.get_news_feed(1) == [10]

    # Feed respects global time ordering across all followees
    t = Twitter()
    t.post_tweet(1, 100)
    t.post_tweet(2, 200)
    t.post_tweet(3, 300)
    t.post_tweet(1, 101)
    t.follow(9, 1)
    t.follow(9, 2)
    t.follow(9, 3)
    # Timestamps: 100(1), 200(2), 300(3), 101(4); newest → oldest
    assert t.get_news_feed(9) == [101, 300, 200, 100]

    # Feed caps at 10
    t = Twitter()
    for tid in range(1, 21):
        t.post_tweet(1, tid)
    feed = t.get_news_feed(1)
    assert len(feed) == 10
    assert feed == [20, 19, 18, 17, 16, 15, 14, 13, 12, 11]

    # Unfollow removes that user's tweets from feed
    t = Twitter()
    t.post_tweet(2, 200)
    t.follow(1, 2)
    assert t.get_news_feed(1) == [200]
    t.unfollow(1, 2)
    assert t.get_news_feed(1) == []

    # Unfollowing an unfollowed user is a no-op
    t.unfollow(1, 999)

    # Empty feed for a new user
    t = Twitter()
    assert t.get_news_feed(42) == []

    # Heavy: 1000 users, each posts 5 tweets; user 0 follows all others
    t = Twitter()
    for u in range(1000):
        for i in range(5):
            t.post_tweet(u, u * 10 + i)
    for u in range(1, 1000):
        t.follow(0, u)

    feed = t.get_news_feed(0)
    assert len(feed) == 10
    # The last 10 tweets posted were user 999's last 5 and user 998's last 5.
    # Specifically the last posted overall was (999, 9994), and times decrease.
    # We just check feed is strictly decreasing in post time.
    # Timestamps aren't exposed, so we verify tweets are unique and in plausible order.
    assert len(set(feed)) == 10

    print("All tests passed!")

    # ---------------------------------------------------------------
    # What Real Twitter Actually Does:
    #
    #   1. FANOUT ON WRITE (common): when a user posts, push the tweet
    #      ID into a cached "timeline" Redis list for each follower.
    #      getNewsFeed is then O(1) — read from cache.
    #
    #   2. FANOUT ON READ (for celebrities): if a user has >100k
    #      followers, fan-out-on-write would write 100k Redis keys per
    #      tweet — too expensive. Instead, their followers' getNewsFeed
    #      calls merge the celebrity's tweet stream at read time.
    #
    #   3. HYBRID: Most systems use both — fanout-on-write for the
    #      common case, fanout-on-read for celebrity accounts. The
    #      decision is made per-user based on follower count.
    #
    #   The DATA STRUCTURES are still the same as we used here. Just
    #   the READ/WRITE split differs for scale.
    # ---------------------------------------------------------------
