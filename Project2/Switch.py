# Project 2 for OMS6250
#
# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.  To 
# remain within the spirit of the project, the only inherited members
# functions the student is permitted to use are:
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# Student code MUST use the send_message function to implement the algorithm - 
# a non-distributed algorithm will not receive credit.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2016 Michael Brown, updated by Kelly Parks 
#           Based on prior work by Sean Donovan, 2015
			    												

from Message import *
from StpSwitch import *

class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):    
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)
        
        #TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree.
        #switchID = self.idNum
        #root = switch id of switch thought to be root origin switch
        self.root = self.switchID
        #print(self.root)
        #distance = distance from origin to root node
        self.distance = 0
        #pathThrough = boolean value indicating the pathe to root from message's origin(the path)
        self.pathThrough = False
        #switchThrough = id value of switch that something goes through
        self.switchThrough = self.switchID
        self.check = False
        self.activeLinks = []
        


    def send_initial_messages(self):
        #TODO: This function needs to create and send the initial messages from this switch.
        #      Messages are sent via the superclass method send_message(Message msg) - see Message.py.
        #      Use self.send_message(msg) to send this.  DO NOT use self.topology.send_message(msg)
        
        for link in self.links:
            claimedRoot = self.root
            distanceToRoot = self.distance
            originID = self.switchID
            destinationID = link
            pathThrough = False
            msg = Message(claimedRoot, distanceToRoot, originID, destinationID, pathThrough)
            self.send_message(msg)
            #print(msg.originID)

        #print(Message.switchID)
        return
        
    def process_message(self, message):
        #TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.
        
        #self.activeLinks.append(self.switchThrough)
        
        if message.pathThrough == True and message.origin not in self.activeLinks:
            self.activeLinks.append(message.origin)
            self.switchThrough = message.origin
        elif message.pathThrough == False and message.origin in self.activeLinks:
            self.activeLinks.remove(message.origin)

        #print(self.activeLinks)
        if (self.root > message.root):
            if(self.switchThrough in self.activeLinks):
                self.activeLinks.remove(self.switchThrough)
            
            self.activeLinks.append(message.origin)
            self.root = message.root
            self.switchThrough = message.origin
            self.distance = message.distance + 1
            self.check = True

        elif(self.distance > message.distance +1 and self.root == message.root):
            if(self.switchThrough in self.activeLinks):
                self.activeLinks.remove(self.switchThrough)
            self.activeLinks.append(message.origin)
            self.switchThrough = message.origin
            self.distance = message.distance + 1
            self.check = True
            
        elif(self.distance == message.distance +1 and self.switchThrough > message.origin):
            self.check = True
            if(self.switchThrough in self.activeLinks):
                self.activeLinks.remove(self.switchThrough)
            self.activeLinks.append(message.origin)
            self.switchThrough = message.origin
           
        
        if self.check is True:
            self.check = False
            for link in self.links:
                claimedRoot = self.root
                distanceToRoot = self.distance
                originID = self.switchID
                destinationID = link
                if self.switchThrough == link:
                    pathThrough = True
                else:
                    pathThrough = False
                msg = Message(claimedRoot, distanceToRoot, originID, destinationID, pathThrough)
                self.send_message(msg)

        


        return
        
    def generate_logstring(self):
        #TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked 
        #      only after the simulaton is complete.  Output the links included in the 
        #      spanning tree by increasing destination switch ID on a single line. 
        #      Print links as '(source switch id) - (destination switch id)', separating links 
        #      with a comma - ','.  
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string 
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.
        
        #self.links.sort()
        #for l in self.links:
        #output = '-'.join(str(*self.links))
        #output += str(l)
        #links = self.links
        #print(*links, sep = "-")
            #link = self.activeLinks
            #print(l)
            #print("%d - %d " % (l,link))
            #print('-'.join(map(str,self.activeLinks)))
        self.activeLinks.sort()
        output = ""
        commasCount = 0
        self.commasCount = len(self.activeLinks)
        #print(self.commasCount)
        for item in self.activeLinks:
            if(self.commasCount == 1):
                output +=  str(self.switchID) + ' - ' + str(item) + "  "
            else:
                output +=  str(self.switchID) + ' - ' + str(item) + ",  "
            self.commasCount -= 1
            print(self.commasCount)


        return (output)
