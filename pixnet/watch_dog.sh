cd /home/peihsuan/pixnet
if [ "$(ps -ef | grep -cw search_result.py)" -lt "36" ]
then
  python3.4 search_result.py&
fi

echo "done"

