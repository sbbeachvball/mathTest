#!/usr/bin/env python
from random import shuffle
import sys
import time

totalQuestions = 100
quizSeconds = 15

class mathTest:
    def __init__(self,total,timer):
        self.stats = {}
        self.stats['counter']   = 0
        self.stats['total']     = total
        self.stats['correct']   = 0
        self.stats['incorrect'] = 0
        self.stats['skipped']   = 0
        self.quizTimer = timer
        
        self.big = []
        # need to generate 200 numbers 0 - 10
        # have a list of which numbers to use, can double up
        self.choices = [ 0,1,2,3,4,5,6,6,6,7,7,7,8,8,8,9,9,10 ]
        while len(self.big) < (self.stats['total'] * 3 ):
            self.big.extend(self.choices)
            
        shuffle(self.big)
        #print self.big
        self.test = self.big[0:(total*2)]
    def is_number(self,s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
    
    def summary(self,s):
        print s
        for s in self.stats:
            print "questions",s,":",self.stats[s]
        
        remaining = self.end - self.now
        if remaining < 0:
            print "Times Up!!"
        else:
            print remaining,"seconds remaining"
    
    def finish(self,s = ''):
        if s :
            print s
            
        self.summary("Final Results")
        sys.exit(0)
        
    def quiz(self,l):
        self.now = int(time.time())
        self.end = self.now + self.quizTimer
        
        # start timer
        # pull two entries off of the list
        while len(self.test) >= 2 and self.now < self.end:
            top = self.test.pop()
            bot = self.test.pop()
            
            self.stats['counter'] += 1
            
            answer = raw_input( "Q%d : what is  %d  X  %d ?: " % (self.stats['counter'],top,bot))
            self.now = int(time.time())
            #print "answer:"+answer+":"
            if answer == "q" or answer == "Q":
                self.finish("Bailing Early")
            elif not self.is_number(answer):
                self.stats['skipped'] += 1
                msg = 'SKIPPED'
            elif ( top * bot ) == int(answer):
                self.stats['correct'] += 1
                msg = "RIGHT!!"
            else:
                self.stats['incorrect'] += 1
                msg = "OOPS - the correct answer is: "+str(top*bot)
        
            self.summary(msg)

        if self.now > self.end:
            self.summary("Times Up!!  Final Results")

mt = mathTest(totalQuestions,quizSeconds)
mt.quiz(mt.test)