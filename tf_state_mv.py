import asyncio
from sysconfig import get_path_names
import os
import glob
import json


path = '/Users/yuyifu/github/file-process/user_maps'
# Open all files in the user_maps directory and process each file one by one
for file in glob.glob(os.path.join(path, '*.txt')):
  # Reset the user list
  users = []
  # file = '/Users/yuyifu/github/file-process/user_maps/user_map_livesocial.txt'
  team_name = file.split('_', 3)[3].replace('.txt','')
  output_file_name = f"tf_state_mv/team_{team_name}.txt"
  
  # Import the data from user_map file to a list of Dictionary users
  with open(file, 'r') as user_map:
    user_map_lines = user_map.readlines()
    for line in user_map_lines:
      user = json.loads(line.replace('\'','\"'))
      users.append(user)
      # print(user)

  # Sore the user list by Email
  users = sorted(users, key=lambda d: d['email']) 

  with open(output_file_name, 'w') as new_tf:
    for user in users:
      new_tf.write(f"terraform state mv -dry-run \'{user['resource']}\' \'module.{team_name}_member.github_team_membership.this[\"{user['email']}\"]\'")
      new_tf.write("\n")
