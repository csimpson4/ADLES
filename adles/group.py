# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging


class Group:
    """ Manages a group of users that has been loaded from a specification """

    def __init__(self, name, group, instance=None):
        """
        :param name: Name of the group
        :param group: Dict specification of the group
        :param instance: Instance number of a template group [default: None]
        """
        logging.debug("Initializing Group '%s'", name)

        if type(group) != dict:
            logging.error("Class Group must be initialized with a dict, not %s: %s",
                          str(type(group)), str(group))
            raise Exception()

        if instance:
            self.is_template = True
            self.instance = instance
        else:
            self.is_template = False

        # !!! NOTE: ad-groups must be handled externally by caller !!!
        if "ad-group" in group:
            group_type = "ad"
            self.ad_group = group["ad-group"]
            users = None
            if instance:  # Template groups
                self.ad_group += " " + str(instance)

        elif "filename" in group:
            from adles.utils import read_json
            group_type = "standard"
            if instance:    # Template group
                users = [(user, pw) for user, pw in read_json(group["filename"])[str(instance)].items()]
            else:           # Standard group
                users = [(user, pw) for user, pw in read_json(group["filename"]).items()]

        elif "user-list" in group:
            group_type = "standard"
            users = group["user-list"]

        else:
            logging.error("Invalid group: %s", str(group))
            raise Exception()

        self.group_type = group_type
        self.users = users
        self.size = int(len(self.users))
        self.name = str(name)
        logging.debug("Finished initializing Group '%s' with %d users", self.name, self.size)


def get_ad_groups(groups):
    """

    :param groups:
    :return:
    """
    ad_groups = []
    for g in groups:
        if type(g) == list:
            for i in g:
                if isinstance(i, Group):
                    ad_groups.append(i)
        elif isinstance(g, Group):
            if g.group_type == "ad":
                ad_groups.append(g)
        else:
            logging.error("Invalid group: %s", str(g))
    return ad_groups
