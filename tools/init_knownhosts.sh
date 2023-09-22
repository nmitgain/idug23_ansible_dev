while read host; do  
  if entry=$(ssh-keyscan $host 2> /dev/null); then  
    echo "$entry" >> ~/.ssh/known_hosts  
  fi 
done < $1 
