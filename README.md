# file-process
Automate some operations to process text files

## Overall Design
1. read_file.py reads the team_members_*.tf files, extracts all the needed user info into a map, and then outputs to the user_map.txt file
1. Manually populate email addresses for each users in the user_map_*.txt files
1. create_new_tf.py creates new team_members_*.tf files for all the teams
1. tf_state_mv.py creates terraform state mv commands for all the teams
