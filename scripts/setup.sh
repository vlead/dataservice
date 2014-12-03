# Updating the packages
apt-get update
echo "Updation done"
# Installing mongodb
apt-get install mongodb
# Installing dependencies
python setup.py install 
# Starting the dataservice
#cd ../src    #Path will be different for test virtual enviroment.
#python app.py
exit 0
