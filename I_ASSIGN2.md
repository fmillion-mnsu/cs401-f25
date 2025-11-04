# Assignment 2: Dealing with Data

In this exercise, we will pretend we're building a processor that is connected to a distance sensor. The idea is that we want to record both an odometer (how far we've traveled in total) as well as a speedometer (based on the last few readings). We also want an "overall average" - the speed average of all recorded events.

While modern builds of MicroPython include Python's Big Integer capabilities, its performance is slow! So, we'll instead use *running average algorithms* to compute our values.

## Assignment:

1. Change your existing MicroPython code to use a **generator** to generate simulated sensor values. The values to be generated should include: 
    - timestamp (for this, just consider this a number of seconds since the start; increment it once for each returned value.)
    - distance traveled (in millimeters) since the last value - you can randomize this within a window to try to indicate a certain "actual speed"

    > Note: We are no longer generating temperature readings - so you can eliminate whatever code you already had generating records for Assignment 1.

2. Change the code to generate **1,000,000** (ten million) entries.
3. Use the **running average** method to keep a computation of the current *overall average*

    The running average algorithm works as follows:

    Each time you add a new value to the array, compute:
    
        new_avg = current_avg + (new_value - current_avg) / count
    
    where `count` is the *new* total number of values we are averaging (hint: increment `count` *before* computing the new average!)

    **Hint:** **Remember order of operations**!

4. Also, use the **running window average** method to keep a computation of the last **60 readings** (the last minute). This will let you compute the average miles-per-hour of travel, based on the last minute of readings.

    This method simply means to use a deque and store the last `n` values along with a running sum of those values. Each time a new value is added once the deque is full, first subtract the value of the first item in the deque from the running total (since that value will be shifted off when you enqueue the next value). Then continue with the usual operation of adding the next value to the running sum and enqueueing in the queue.

5. Add computations to display your calculations in miles-per-hour (remember, your virtual sensor should output *millimeters traveled*). You should display:

* A running window average of the last 60 records every 60 "seconds" (i.e. every 60 generated records - it will run much faster than one record per second!)
* The *overall average* of *all readings* (by using the running average method from Step 3)
* The total number of records processed - you can just print whatever static value you've decided on.

## Hints

* Make your generator flexible - have it accept a value for the number of records to generate. 
* Test with smaller record sets first - try generating just 600 records, and also keep your existing code to compute the average traditionally (summing all values and dividing). Make sure your average works properly! Then remove the traditional sum-all-values average code and use only the rolling average code.

# Submission

Your submission must include:

* The code for your updated version of the program that can run successfully

Submit your work to D2L no later than *Monday, November 10th* at 11:59 PM.

## Grading

This assignment is worth **100 points**.

Components:

| Item | Points | Scoring |
|-|-|-|
| Evidence of Hello World | 15 | Full points if Hello World program shown working. Zero points if omitted. |
| Evidence of Unoptimized Program Crash | 15 | Full points if crash is shown. Zero points if not done. |
| Optimized Program | 70 | Full points if updated program runs successfully and still does all of the same work - it must compute 5,000 random records with all the given fields and compute the average temperature of all data records. It should then print that average temperature before exiting. Points are taken off for buggy code, incorrect logic, or code that is incomplete or can't be run. |
