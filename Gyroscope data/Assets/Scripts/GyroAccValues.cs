using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.IO;

public class GyroAccValues : MonoBehaviour
{
    Quaternion gyroAttitude, old_gyroAttitude;
    Vector3 gyroRotationRate, old_gyroRotationRate;
    Vector3 acceleration, old_acceleration;
    public Text gyro11, gyro12, gyro13, gyro21, gyro22, gyro23, acc1, acc2, acc3, refreshRate, startStop, gravity1, gravity2, gravity3;
    //----------Output--------------
    public Slider bgNoise;
    public TMPro.TMP_Dropdown lang, distance,numPers, numMale, numFemale;
    public TMPro.TMP_InputField years1, years2, years3, years4, years5, years6, words;
    public Text outLabel;
    //------------------------------
    StreamWriter writerGyroAtt, writerGyroRot, writerAcc, writerOutput;
    bool writingInput = false, writingOutput = false;
    float timer = 0.0f, writeTimer = 0.0f, startRecordingTime;
    AudioClip record;
    string date;
    // Start is called before the first frame update
    void Start()
    {
        Input.gyro.enabled = true;
        gyroAttitude = new Quaternion(0, 0, 0, 0);
        gyroRotationRate = new Vector3(0, 0, 0);
        acceleration = new Vector3(0, 0, 0);
        Input.gyro.updateInterval = 0.005f;
        refreshRate.text = (1f / Input.gyro.updateInterval).ToString();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        old_gyroAttitude = gyroAttitude;
        old_gyroRotationRate = gyroRotationRate;
        old_acceleration = acceleration;

        gyroAttitude = Input.gyro.attitude;
        gyroRotationRate = Input.gyro.rotationRateUnbiased;
        acceleration = Input.acceleration;

        /*gyro11.text = ((gyroAttitude.x - old_gyroAttitude.x) * 1000).ToString();
        gyro12.text = ((gyroAttitude.y - old_gyroAttitude.y) * 1000).ToString();
        gyro13.text = ((gyroAttitude.z - old_gyroAttitude.z) * 1000).ToString();
        gyro14.text = ((gyroAttitude.w - old_gyroAttitude.w) * 1000).ToString();
        gyro21.text = ((gyroRotationRate.x - old_gyroRotationRate.x) * 1000).ToString();
        gyro22.text = ((gyroRotationRate.y - old_gyroRotationRate.y) * 1000).ToString();
        gyro23.text = ((gyroRotationRate.z - old_gyroRotationRate.z) * 1000).ToString();
        acc1.text = ((acceleration.x - old_acceleration.x) * 1000).ToString();
        acc2.text = ((acceleration.y - old_acceleration.y) * 1000).ToString();
        acc3.text = ((acceleration.z - old_acceleration.z) * 1000).ToString();*/

        gyro11.text = (gyroAttitude.x).ToString();
        gyro12.text = (gyroAttitude.y).ToString();
        gyro13.text = (gyroAttitude.z).ToString();
        gyro21.text = (gyroRotationRate.x).ToString();
        gyro22.text = (gyroRotationRate.y).ToString();
        gyro23.text = (gyroRotationRate.z).ToString();
        acc1.text = (acceleration.x - Input.gyro.gravity.x).ToString();
        acc2.text = (acceleration.y - Input.gyro.gravity.y).ToString();
        acc3.text = (acceleration.z - Input.gyro.gravity.z).ToString();
        gravity1.text = Input.gyro.gravity.x.ToString();
        gravity2.text = Input.gyro.gravity.y.ToString();
        gravity3.text = Input.gyro.gravity.z.ToString();

        if (writingInput)
        {
            writerGyroAtt.WriteLine(gyroAttitude.x.ToString() + "\t" + gyroAttitude.y.ToString() + "\t" + gyroAttitude.z.ToString());
            writerGyroRot.WriteLine(gyroRotationRate.x.ToString() + "\t" + gyroRotationRate.y.ToString() + "\t" + gyroRotationRate.z.ToString());
            writerAcc.WriteLine((acceleration.x - Input.gyro.gravity.x).ToString() + "\t" + (acceleration.y - Input.gyro.gravity.y).ToString() + "\t" + (acceleration.z - Input.gyro.gravity.z).ToString());
            if (timer - writeTimer >= 59.995)
                stopWriteData();
        }

        timer += Time.deltaTime;
    }

    public void startWriteData()
    {
        if (!writingOutput)
        {
            openFiles();
            startStop.text = "Started, please wait...";
            writeTimer = timer;
            writingInput = true;
            Debug.Log("Poceo");
            startRecording();
        }
    }

    public void stopWriteData()
    {
        writingInput = false;
        writerGyroAtt.Close();
        writerGyroRot.Close();
        writerAcc.Close();
        startStop.text = "Finished!";
        stopRecording();
        writingOutput = true;
        Debug.Log("Zavrsio");
    }

    public void openFiles()
    {
        System.DateTime dateTime = System.DateTime.Now;
        date = "" + dateTime.Day + dateTime.Month + dateTime.Year + dateTime.Hour + dateTime.Minute + dateTime.Second;
        FileStream fileGyroAtt = File.Open(Application.persistentDataPath + "/GyroscopeAttitude" + date + ".txt", FileMode.OpenOrCreate, FileAccess.ReadWrite);
        FileStream fileGyroRot = File.Open(Application.persistentDataPath + "/GyroscopeRotRate" + date + ".txt", FileMode.OpenOrCreate, FileAccess.ReadWrite);
        FileStream fileAcc = File.Open(Application.persistentDataPath + "/Acceleration" + date + ".txt", FileMode.OpenOrCreate, FileAccess.ReadWrite);
        FileStream fileOut = File.Open(Application.persistentDataPath + "/Output" + date + ".txt", FileMode.OpenOrCreate, FileAccess.ReadWrite);
        Debug.Log(Application.persistentDataPath + "/Output" + date + ".txt");
        writerGyroAtt = new StreamWriter(fileGyroAtt);
        writerGyroRot = new StreamWriter(fileGyroRot);
        writerAcc = new StreamWriter(fileAcc);
        writerOutput = new StreamWriter(fileOut);
        writerGyroAtt.WriteLine("x" + "\t" + "y" + "\t" + "z");
        writerGyroRot.WriteLine("x" + "\t" + "y" + "\t" + "z");
        writerAcc.WriteLine("x" + "\t" + "y" + "\t" + "z");
        writerOutput.WriteLine("BgNoise" + "\t" + "Lang" + "\t" + "Dist" + "\t" + "#Pers" + "\t" + "#M" + "\t" + "#F" + "\t" + "Y1" + "\t" + "Y2" + "\t" + "Y3"
                + "\t" + "Y4" + "\t" + "Y5" + "\t" + "Y6" + "\t" + "Letter/Num/Word..");

    }

    public void startRecording()
    {
        int minFreq;
        int maxFreq;
        int freq = 44100;
        Microphone.GetDeviceCaps("", out minFreq, out maxFreq);
        Debug.Log("Min freq: " + minFreq + " Max freq: " + maxFreq);
        if (maxFreq < 44100)
            freq = maxFreq;
        record = Microphone.Start("", false, 300, freq);
        startRecordingTime = Time.time;
    }

    public void stopRecording()
    {
        Microphone.End("");
        //-----Trimming audio file-----
        AudioClip temp = AudioClip.Create("Recording" + date, (int)((Time.time - startRecordingTime) * record.frequency), record.channels, record.frequency, false);
        float[] data = new float[(int)((Time.time - startRecordingTime) * record.frequency)];
        record.GetData(data, 0);
        temp.SetData(data, 0);
        record = temp;
        //-----Saving to wav fromat-------
        SavWav.Save("Recording" + date, record);

    }

    public void writeOutput()
    {
        if (writingOutput)
        {
            writerOutput.WriteLine(decimal.Round((decimal)bgNoise.value, 2, System.MidpointRounding.AwayFromZero) + "\t" + lang.captionText.text + "\t" + distance.captionText.text + "\t" + numPers.captionText.text
                + "\t" + numMale.captionText.text + "\t" + numFemale.captionText.text + "\t" + years1.text + "\t" + years2.text + "\t" + years3.text
                + "\t" + years4.text + "\t" + years5.text + "\t" + years6.text + "\t" + words.text);
            writerOutput.Close();
            writerGyroAtt.Close();
            writerGyroRot.Close();
            writerAcc.Close();
            outLabel.text = "Finished";
            writingOutput = false;
            Debug.Log("Zavrsio ispis outputa"+ bgNoise.value);
        }
    }
}
