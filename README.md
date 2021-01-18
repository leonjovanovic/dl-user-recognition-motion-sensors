# Application of deep learning algorithms in user recognition based on motion sensors.

## Summary
  Goal of the thesis is to find out if it possible to find some attributes of speakers who are speaking near smartphone in idle state (on nearby horizontal surface) based on values from accelerometer and gyroscope. Accelerometer and gyroscope are very sensitive sensors which means they will catch some vibrations even though phone is not moving. We will then input sensor values into deep learning algorithm to learn based on output we manually created for each test. 

  We will try to predict 
  * background noise (low, medium, high)
  * language (Serbian, English, German)
  * distance from phone (0-2, 3-5, 5+ meters)
  * number of people speaking (1, 2, 3, 4, 5, 6+)
  * at least 1 male
  * at least 1 female
  * speakers years (<18, 18-30, >30)
  * certain letters or words ('a', 'knjiga', 'letter', 'schmetterling')

## Collecting data
  The first part of the thesis was data collection, which will be later entered into the algorithm. One test represents 60 seconds of recording data from the accelerometer and gyroscope in unique situations at a frequency of 200Hz. One situation is a combination of characteristics such as number, gender, location, age and language of the speaker. 315 tests were performed for a certain period of time. Collecting is done with small Unity application which will generate input (sensor values) and output (speaker attributes).
  
![](images/unity_data.jpg)
*image_caption*
<p style="text-align: center;">Centered text</p>

  


