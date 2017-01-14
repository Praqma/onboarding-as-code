echo "Building $TRAVIS_BRANCH"
echo "Commit: $TRAVIS_COMMIT"

TEST_ACCOUNT="travis.yaml"
TEST_DIRECTORY="$PWD/test_directory"
TEST_GOOGLE_KEY="$PWD/test_credentials/key.json"
TEST_GOOGLE_ADMIN_EMAIL="admin@sysdevprosup.org"

# Activate virtual env
source env/bin/activate

# Add test record
cat > ${TEST_ACCOUNT} << EOF
!!python/object:lib.person.Person
email: travis@gmail.com
fname: Travis
lname: Travisson
gid: travis.github
pid: trs
EOF

# Copy account to directory
cp ${TEST_ACCOUNT} ${TEST_DIRECTORY}/

# Add account dry run mode
python main.py -n -d -p ${TEST_DIRECTORY} -k ${TEST_GOOGLE_KEY} -e ${TEST_GOOGLE_ADMIN_EMAIL} add
printf "\n\n\n\n"

# Delete account from directory
rm -f ${TEST_DIRECTORY}/${TEST_ACCOUNT}

# Delete account dry run mode
python main.py -n -d -p ${TEST_DIRECTORY} -k ${TEST_GOOGLE_KEY} -e ${TEST_GOOGLE_ADMIN_EMAIL} del
printf "\n\n\n\n"

# Copy account to directory
cp ${TEST_ACCOUNT} ${TEST_DIRECTORY}/

# Add account
python main.py -d -p ${TEST_DIRECTORY} -k ${TEST_GOOGLE_KEY} -e ${TEST_GOOGLE_ADMIN_EMAIL} add
printf "\n\n\n\n"

# Delete account from directory
rm -f ${TEST_DIRECTORY}/${TEST_ACCOUNT}

# Delete account
python main.py -d -p ${TEST_DIRECTORY} -k ${TEST_GOOGLE_KEY} -e ${TEST_GOOGLE_ADMIN_EMAIL} del
printf "\n\n\n\n"

# Test docker build
docker build -t onboarding .

echo "Ok"
