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
  output_file_name = f"new_team_files/team_members_{team_name}.tf"
  
  # Import the data from user_map file to a list of Dictionary users
  with open(file, 'r') as user_map:
    user_map_lines = user_map.readlines()
    for line in user_map_lines:
      user = json.loads(line.replace('\'','\"'))
      users.append(user)
      # print(user)

  # Sore the user list by Email
  users = sorted(users, key=lambda d: d['email']) 

  # Get all the roles in a set
  roles = set( dic['role'] for dic in users)
  # print(roles)

  # Output user maps by role
  with open(output_file_name, 'w') as new_tf:
    new_tf.write("locals {")
    new_tf.write("\n")

    for role in roles:
      new_tf.write(f"  {team_name}_{role} = tomap({{")
      new_tf.write("\n")
      for user in users:
        if user['role'] == role:
          new_tf.write(f"    \"{user['email']}\" = \"{user['username']}\"")
          new_tf.write("\n")
      new_tf.write("  })")
      new_tf.write("\n")      
    
    new_tf.write("}")
    new_tf.write("\n")

    # Output codes that call module for each role
    for role in roles:
      new_tf.write(f"module \"{team_name}_{role}\" {{")
      new_tf.write("\n")
      new_tf.write("  source  = \"../modules/team-members\"")
      new_tf.write("\n")
      new_tf.write(f"  members = local.{team_name}_{role}")
      new_tf.write("\n")
      new_tf.write(f"  team_id = github_team.{team_name}_team.id")
      new_tf.write("\n")
      new_tf.write(f"  role    = \"{role}\"")
      new_tf.write("\n")    
      new_tf.write("}")
      new_tf.write("\n")
      new_tf.write("\n")
