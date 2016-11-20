#!/usr/bin/env python
from random import shuffle
import sys
import time

# normal ratio is 5 minutes for 100 questions, so 20 questions per minute
totalQuestions = 50
quizSeconds = 170
#quizSeconds = 10

class mathTest:
    def __init__(self,total,timer):
        self.stats = {}
        self.stats['counter']   = 0
        self.stats['total']     = total
        self.stats['correct']   = 0
        self.stats['incorrect'] = 0
        self.stats['skipped']   = 0
        self.stats['answered']  = 0
        self.quizTimer = timer
        self.corrections = ''
        self.corrections += '\n###################################'
        self.corrections += '\n######  Corrected Answers:   ######\n'
        
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
    
    def summary(self,s,remainingSecs = True):
        print s
        summ = 'questions - answered: %d of %d, correct: %d, incorrect: %d, skipped: %d' % (self.stats['answered'],self.stats['total'],self.stats['correct'],self.stats['incorrect'],self.stats['skipped'])
        #summ = 'questions - answered: %d, correct: %s, incorrect: %s' % (self.stats['answered'],self.stats['correct'],self.stats['incorrect'])
        #for st in self.stats:
        #    print "questions",st,":",self.stats[st]
        print summ
        
        remaining = self.end - self.now
        if remainingSecs and remaining >= 0:
            print remaining,"seconds remaining"
        print "##########################################################################"

    def carryOn(self,s = ''):
        self.summary(s)

    def finish(self,s = ''):
        self.summary(s+" - Final Results",False)
        self.finalGrade()
        sys.exit(0)
        
    def remainingAnswers(self):
        if len(self.test) < 2:
            return
            
        print '\n'
        print '###################################'
        print '######  Remaining Questions  ######'
        print '###################################'
        while len(self.test) >= 2:
            top = self.test.pop()
            bot = self.test.pop()
            print "%d X %d = %d" % (top,bot,(top*bot))
        
    def finalGrade(self):
        print ""
        if self.stats['incorrect'] > 0:
            print self.corrections
            
        self.remainingAnswers()
            
        print ""
        print '###################################'
        print '######  Final Grade: %5.1f%%  ######' % (float(self.stats['correct']) / float(self.stats['total']) * 100)
        print '###################################'
        
    def update(self,dct):
        for dk in dct:
            self.stats[dk] += dct[dk]
        self.stats['answered'] = self.stats['incorrect'] + self.stats['correct']
        
    def stashErrors(self,top,bot,answer):
        self.corrections += '%2d X %2d = %2d   --   Your incorrect answer was: %3s\n' % (top,bot,(top*bot),answer)

    def quiz(self,l):
        # start timer
        self.now = int(time.time())
        self.end = self.now + self.quizTimer
        
        # while there is still time ask the next question
        while len(self.test) >= 2 and self.now < self.end:
            # pull two entries off of the list
            top = self.test.pop()
            bot = self.test.pop()
            
            self.stats['counter'] += 1
            
            answer = raw_input( "Q#%d : what is  %d  X  %d ?: " % (self.stats['counter'],top,bot))
            
            # get the answer time....
            self.now = int(time.time())
            #print "answer:"+answer+":"
            
            # should probably check time BEFORE evaluating the answer
            if self.now > self.end:
                self.finish("Sorry, time ran out")
            elif answer == "q" or answer == "Q":
                self.finish("Bailing Early")
            elif not self.is_number(answer):
                self.test.insert(0,top)
                self.test.insert(0,bot)
                self.update({ 'skipped': 1})
                self.carryOn('SKIPPED')
            elif ( top * bot ) == int(answer):
                self.update({ 'correct': 1})
                self.carryOn("RIGHT!!")
            else:
                self.update({ 'incorrect': 1})
                self.stashErrors(top,bot,answer)
                self.carryOn("OOPS - You answered incorrectly")
        
        # if we ran out of time before getting here, issue appropriate message
        if self.now >= self.end:
            self.finish("Times Up!!")
        else:
            self.finish("WOW!! You completed the test with time to spare")
            
        

mt = mathTest(totalQuestions,quizSeconds)
mt.quiz(mt.test)