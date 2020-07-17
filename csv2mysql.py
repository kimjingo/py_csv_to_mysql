#!/usr/bin/python3
import csv
import pymysql
# import numpy

## create table manualposts
sql = "CREATE IF NOT EXISTS TABLE `manualposts` ( \
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT, \
    `pdate` date NOT NULL, \
    `amt` decimal(8,2) NOT NULL, \
    `mp` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT '', \
    `cr` char(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL, \
    `cr_dir` tinyint(4) DEFAULT NULL, \
    `cr_clearing` char(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL, \
    `dr` char(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL, \
    `dr_dir` tinyint(4) DEFAULT NULL, \
    `dr_clearing` char(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL, \
    `material` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT '', \
    `remark` char(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL, \
    `ttype` char(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL, \
    `checkno` char(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL, \
    `posting` date DEFAULT NULL, \
    `paidby` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT '', \
    `ba` tinyint(4) DEFAULT NULL, \
    `created_at` timestamp NULL DEFAULT NULL, \
    `updated_at` timestamp NULL DEFAULT NULL, \
    `filename` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL, \
    PRIMARY KEY (`id`), \
    UNIQUE KEY `manualposts_pdate_amt_mp_remark_checkno_ttype_unique` (`pdate`,`amt`,`mp`,`remark`,`checkno`,`ttype`) \
) ENGINE=InnoDB AUTO_INCREMENT=3772 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci "

# Open database connection
mydb = pymysql.connect(host="localhost",
                    user="user",
                    passwd="password",
                    db="db1",
                    port=3306 )


# prepare a cursor object using cursor() method
cursor = mydb.cursor()

# create table if not exists
try:
    cursor.execute(sql)
    mydb.commit()
except:
    print ("Error: unable to create table")

with open('../hanmi.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(csvreader)
    for row in csvreader:
        account_no = row[0]
        post_date = row[1]
        check_no = row[2]
        desc = row[3]
        debit = row[4]
        credit = row[5]
        status = row[6]
        balance = row[7]
        if(debit=="") :
            debit=0
        if(credit=="") :
            credit=0
        amt = float(debit) - float(credit)

        sql = "INSERT INTO manualposts(pdate, amt, checkno, paidby, remark ) VALUE (STR_TO_DATE('%s','%%c/%%e/%%Y'), %d, '%s', '%s', '%s')" % (post_date, amt, check_no, account_no, desc)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            mydb.commit()
        except:
            print ("Error: unable to insert data")



sql = "SELECT * FROM manualposts WHERE id > 3771"
try:
    # Execute the SQL command
    cursor.execute(sql)
    # Fetch all the rows in a list of lists.
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        pdate = row[1]
        amt = row[2]
        mp = row[3]
        remark = row[11]
        checkno = row[13]
        paidby = row[15]
        # Now print fetched result
        print ("id = %d,pdate = %s,amt = %d,remark = %s, checkno=%s, paidby=%s" % \
        (id, pdate, amt, remark, checkno, paidby ))
except:
    print ("Error: unable to fetch data")

# disconnect from server
mydb.close()