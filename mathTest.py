#!/usr/bin/env python
from random import shuffle
import sys
import time
import argparse


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--q_num', default=50, type=int, help='number of questions in quiz')
parser.add_argument('--q_dur', default=175, type=int, help='number of seconds for the quiz duration')
parser.add_argument('--debug', action='store_false', help='debug mode')

args = parser.parse_args()

#print 'questions:',args.q_num
#print 'quiztime:',args.q_dur

#sys.exit(0)
# normal ratio is 5 minutes for 100 questions, so 20 questions per minute

# this isn't used but is a nice subroutine that could be useful for my
# padStr below.
def rep(s, m):
    a, b = divmod(m, len(s))
    return s * a + s[:b]

# s is the string to pad
# p is the pad characters
# l is the length to pad things out to
# spad is used to surround s with before padding unless len(s) == 0
def padStr(s = '',spad = ' ', p = '#', l = 60):
    sl = len(s)
    if sl == 0:
        spad = ''
        
    pl = l - sl - (len(spad) * 2)
    if pl <= 0:
        if args.debug:
            print 'string too long to pad, sorry'
        return s
    mod = pl % 2
    fpad = pl / 2
    rpad = pl / 2 + mod
    return p*fpad+spad+s+spad+p*rpad

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
        self.corrections += '\n'+padStr()
        self.corrections += '\n'+padStr('Corrected Answers:')+'\n'
        self.remaining = 0
        self.earned = 0
        
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
        
        self.remaining = self.end - self.now
        if remainingSecs and self.remaining >= 0:
            print self.remaining,"seconds remaining"
        print padStr()

    def carryOn(self,s = ''):
        self.summary(s)

    def instructions(self):
        print "The controls are as follows:"
        print "  space - skips to next question"
        print "  q     - exit now"
        print "  x     - exit now"
        print ""
        #print "Hit return to begin:"
        raw_input("Hit return to begin!")
        
    def beg(self):
        self.now = int(time.time())
        self.end = self.now + self.quizTimer        
        
    def finish(self,s = ''):
        self.summary(s+" - Final Results",False)
        self.finalGrade()
        sys.exit(0)
        
    def remainingAnswers(self):
        if len(self.test) < 2:
            return
            
        print '\n'
        print padStr()
        print padStr('%d' % (len(self.test)/2) + ' Remaining Questions')
        print padStr()
        while len(self.test) >= 2:
            top = self.test.pop()
            bot = self.test.pop()
            print "%d X %d = %d" % (top,bot,(top*bot))
    
    def timeEarned(self):
        self.earned = {}
        self.earned['perc'] = 0
        self.earned['time'] = 0
                
        perc = int((float(self.stats['correct']) / float(self.stats['total']) * 100))
        self.earned['time'] = self.remaining if self.remaining > 0 and perc > 85 else 0
        
        self.earned['perc'] =  (perc - 85) if perc > 85 else 0            
        self.earned['total'] = self.earned['time'] + self.earned['perc']
        
        print ""
        print padStr()
        print padStr("You earned: "+str(self.earned['total'])+" minutes ("+str(self.earned['time'])+" secs + " + str(self.earned['perc']) +" perc)")
        print padStr()
        
    def finalGrade(self):
        print ""
        if self.stats['incorrect'] > 0:
            print self.corrections
            
        self.remainingAnswers()
            
        print ""
        print padStr()
        print padStr('Final Grade: %5.1f%%' % (float(self.stats['correct']) / float(self.stats['total']) * 100))
        print padStr()
        
        self.timeEarned()
        
    def update(self,dct):
        for dk in dct:
            self.stats[dk] += dct[dk]
        self.stats['answered'] = self.stats['incorrect'] + self.stats['correct']
        
    def stashErrors(self,top,bot,answer):
        self.corrections += '%2d X %2d = %2d   --   Your incorrect answer was: %3s\n' % (top,bot,(top*bot),answer)

    def quiz(self,l):
        self.beg()
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
            elif answer == "q" or answer == "Q" or answer == 'x' or answer == "X":
                self.finish("Bailing Early")
            elif not self.is_number(answer):
                self.test.insert(0,top)
                self.test.insert(0,bot)
                self.update({ 'skipped' : 1})
                self.update({ 'counter' : -1})
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
            
        

mt = mathTest(args.q_num,args.q_dur)
mt.quiz(mt.test)
#print padStr('#')
#print padStr('')
#print padStr('Final Results !!','  ')
#print padStr('Answered questions')
#print padStr('Yay!')
