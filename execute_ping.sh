# !/usr/bin
# coding: utf-8

MINION_FILE='ips.txt'
ok='./ping_ok'
err='./ping_err'
res='./ping_result'

rm -f $ok $err $res

while read minion
do
  ping $minion -c 1 -w 1 > ./tmp.txt
  if [ $? -eq 0 ];then
    # cat ./tmp.txt
    echo "${minion} ping ok."
    echo -e "${minion} OK" >> $ok
    echo -e "OK" >> $res
  else
    echo "${minion} ping error."
    echo -e "${minion} ERROR" >> $err
    echo -e "不通" >> $res
  fi
done < $MINION_FILE
