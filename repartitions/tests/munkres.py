import json

import numpy as np

from associations.tests.base_test import BaseTestCase
from authentication.models import User
from repartitions.algorithm import get_project_index
from repartitions.models import Proposition, Campaign, UserCampaign, Category, Wish


class MunkresTestCase(BaseTestCase):

    fixtures = ['authentication.yaml', 'test_repartition_api.yaml']

    def test_get_project_index(self):
        self.assertEqual(4, get_project_index(5, {1, 1, 1, 1, 1}))
        self.assertEqual(1, get_project_index(5, {3, 3, 3}))
        self.assertEqual(0, get_project_index(0, {1, 3, 3}))
        self.assertEqual(1, get_project_index(1, {1, 3, 3}))
        self.assertEqual(2, get_project_index(0, {0, 0, 3}))
        self.assertEqual(5, get_project_index(1, {0, 0, 1, 0, 0, 1}))

    def generate_batch_wishes(self):
        np.random.seed(0)

        campaign = Campaign(name="Batch campaign", manager_id="17bocquet")
        campaign.save()

        propositions = []
        for i in range(10):
            proposition = Proposition(
                campaign_id=campaign.id,
                name="proposition_{}".format(i),
                number_of_places=10
            )
            proposition.save()
            propositions.append(proposition)

        categories = []
        for name in ["category_{}".format(i) for i in range(4)]:
            category = Category(name=name)
            category.save()
            categories.append(category)

        user_campaigns = []
        for i in range(168):
            user = User(
                id="19user{}".format(i),
                first_name="firstname {}".format(i),
                last_name="lastname {}".format(i),
                promo=19,
                email="email{}@mpt.fr".format(i),
            )
            user.save()

            category = np.random.choice(categories, 1, p=[0.8, 0.1, 0.06, 0.04])[0]
            uc = UserCampaign(
                user=user,
                campaign=campaign,
                category=category
            )
            uc.save()
            user_campaigns.append(uc)

            if i < 157:  # simulate that a few users didn't answer the form
                for (rank, proposition) in enumerate(np.random.permutation(propositions)):
                    wish = Wish(
                        user=user,
                        proposition=proposition,
                        rank=rank
                    )
                    wish.save()

        return campaign, propositions, categories, user_campaigns

    def test_reparition_is_even(self):
        campaign, _, categories, _ = self.generate_batch_wishes()
        self.login("17bocquet")
        res = self.get("/repartition/{}/results/".format(campaign.id))
        self.assertEqual(res.status_code, 200)
        groups = json.loads(res.content)["groups"]

        # Checks that categories are evenly shared
        counts = {category.id: [] for category in categories}
        for group in groups:
            count = {category.id: 0 for category in categories}
            for user in group["users"]:
                count[user["category"]] += 1

            for k in counts.keys():
                counts[k].append(count[k])

        for c in counts.values():
            m, M = min(c), max(c)
            self.assertLessEqual(M - m, 1)

        # Checks that all groups have about the same number of people in them
        user_count = [len(group["users"]) for group in groups]
        m, M = min(user_count), max(user_count)
        self.assertLessEqual(M - m, 1)

    def test_respects_fixity(self):
        campaign, propositions, _, user_campaigns = self.generate_batch_wishes()

        users_to_fix = 9
        uc_to_fix = np.random.choice(user_campaigns, users_to_fix, replace=False)
        propositions_to_fix = np.random.choice(propositions, users_to_fix, replace=True)

        expectations = {}
        for (uc, proposition) in zip(uc_to_fix, propositions_to_fix):
            if proposition.id not in expectations:
                expectations[proposition.id] = []
            expectations[proposition.id].append(uc.user.id)

            uc.fixed_to = proposition
            uc.save()

        self.login("17bocquet")
        res = self.get("/repartition/{}/results/".format(campaign.id))
        self.assertEqual(res.status_code, 200)
        groups = json.loads(res.content)["groups"]

        for group in groups:
            to_find = expectations[group["proposition"]["id"]]
            for user in group["users"]:
                if user["id"] in to_find:
                    to_find.remove(user["id"])
            self.assertEqual(len(to_find), 0)
