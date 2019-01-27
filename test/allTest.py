import shipsTest
import buildingTest
import planesTest
import roadsTest
import vegetationTest

print("TESTING BASE OBJECTS\n")
print("############\n")
print("testing ships:")
shipsTest.run_test()
print("\ntesting planes:")
planesTest.run_test()
print("\nTESTING BASE MAPS\n")
print("############\n")
print("\ntesting buildings:")
buildingTest.run_test()
print("\ntesting roads:")
roadsTest.run_test()
print("\ntesting vegetations:")
vegetationTest.run_test()
