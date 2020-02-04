#!/bin/bash

# create nCoV.sh
echo '#!/bin/bash' > nCoV.sh
echo -n 'cd ' >> nCoV.sh
echo `pwd` >> nCoV.sh
echo 'source ./venv/bin/activate' >> nCoV.sh
echo 'python3 nCoV.py' >> nCoV.sh

# create nCoV.sh
echo '#!/bin/bash' > nCoV-notweet.sh
echo -n 'cd ' >> nCoV-notweet.sh
echo `pwd` >> nCoV-notweet.sh
echo 'source ./venv/bin/activate' >> nCoV-notweet.sh
echo 'python3 nCoV.py --notweet' >> nCoV-notweet.sh

# create nCoV.sh
echo '#!/bin/bash' > nCoV-nopickle.sh
echo -n 'cd ' >> nCoV-nopickle.sh
echo `pwd` >> nCoV-nopickle.sh
echo 'source ./venv/bin/activate' >> nCoV-nopickle.sh
echo 'python3 nCoV.py --nopickle' >> nCoV-nopickle.sh

# create nCoV.sh
echo '#!/bin/bash' > nCoV-notweet-nopickle.sh
echo -n 'cd ' >> nCoV-notweet-nopickle.sh
echo `pwd` >> nCoV-notweet-nopickle.sh
echo 'source ./venv/bin/activate' >> nCoV-notweet-nopickle.sh
echo 'python3 nCoV.py --notweet --nopickle' >> nCoV-notweet-nopickle.sh

chmod u+x nCoV*.sh