from sysconfig import get_path_names
import os
import glob

path = '/Users/yuyifu/github/file-process/team_members'
# Open all files in the team_member directory and process each file one by one
for file in glob.glob(os.path.join(path, '*.tf')):
  print(file)
  # Create a new empty file to store user info in a mpa
  output_file_name = file.split('_', 3)[3].replace('.tf','')
  user_map = open(f"user_maps/user_map_{output_file_name}.txt", 'w')
  user_map.close
  # Read the team_member_*.tf file line by line
  with open(file, 'r') as team_file:
    teamlines = team_file.readlines()
    for line in teamlines:

      # If the line is a comment, skip to the next line
      if '#' in line:
        if line.strip()[0] == '#':
          continue

      if "resource \"github_team_membership\"" in line:
        # When it comes to a new resource block, reset the user dictionary
        user=dict({'resource': '', 'team': '', 'username': '', 'role': '', 'email': ''})
        # Retrieve origin resource name
        user['resource'] = line.split()[1].replace('"','')+'.'+line.split()[2].replace('"','')
        # Retrieve team name
        
      if "team_id" in line:
        user['team'] = line.split('.')[1].strip().replace('_team','')
        # print(user['team'])

      # Retrieve user GitHub username
      if "username" in line:
        user['username'] = line.split('=')[1].strip().replace('"','').replace('\n','')
        # print(user['username'])
      
      # Retrieve user role
      if "role" in line:
        user['role'] = line.split(' = ')[1].strip().replace('"','').replace('\n','')
        # print(user['role'])

      # Add the user info to the output user map file
      if "}" in line:
        # Append the user info the map file
        with open(f"user_maps/user_map_{output_file_name}.txt", 'a') as user_map:
          user_map.write(str(user))
          user_map.write('\n')
        # print(user)
