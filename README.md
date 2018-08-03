# FRB_VOEvent
A VOEvent standard for fast radio bursts

In this repository you will find the most up-to-date information about FRB VOEvents: why use them, how to make them, and how to receive them.

## What is a VOEvent?

A VOEvent is a communication standard developed by the Virtual Observatory to send information on short timescales about new astronomical events. A VOEvent is an xml schema that contains important/relevant information about a new event so that others around the world can follow up and take more data after the event has been reported. You can read more about the VOEvent concept [here](http://voevent.readthedocs.io/en/latest/#)

A VOEvent contains a few different _elements_ to break up the information into a few different categories:
* Who is issuing the event?
* What is the event of interest?
* Where/When did the event occur?
* Why should this event be followed up?

VOEvents are sent over the VOEvent network. They are issued by an _author_ using a broker and are either received by a _subscriber_ or received and then re-transmitted by an intermediary broker and then received by the subscribers to the second broker.

## Why VOEvents?

VOEvents allow you to communicate very quickly with other people listening in to the network around the world. The events themselves are machine generated and machine parsable (see below) so they are ideal for robotic telescopes or for real-time search pipelines that operate with minimal or no human intervention.

### Why VOEvents for FRBs?

There are a lot of reasons why we believe VOEvents are really great for FRB detection and follow-up. There are so many reasons, in fact, that we wrote a paper! Please read the paper in this repository (FRB_VOEvent_Paper_\*.pdf) for the details of the FRB VOEvent standard and the justification behind FRB VOEvents. All the parameters used in these events are defined in parameter_definitions.pdf and a table schematic of where these parameters are used and/or required is provided in the parameter_table.pdf document.

## Interacting with VOEvents

VOEvents are `xml` files, meaning you can just interact with them by editing the text they contain. That's not the nicest way, though. There are great tools that have already been created for manipulating and interacting with VOEvents in python. The one used here and in many implementations is `voeventparse`. You can learn more at the [voeventpares tutorial page](http://voevent-parse.readthedocs.io/en/latest/tutorial/index.html). 

This is as far as you need to read if you were just interested in VOEvents in general. If you're more specifically interested in _FRB VOEvents_ keep reading!

## Authoring an FRB VOEvent

This repository contains tools for creating FRB VOEvents. The [templates](https://github.com/ebpetroff/FRB_VOEvent/tree/master/templates) directory contains blank VOEvents of all the different types described in the paper. The [examples](https://github.com/ebpetroff/FRB_VOEvent/tree/master/examples) directory contains a few simple examples of what a detection and update event would look like for a given FRB. The (SCRIPTS) directory contains some basic scripts for creating a basic detection FRB message. The READMEs in the different directories contain more information about usage.

## Issuing your VOEvent

The FRB Catalogue (FRBCAT) will very soon run a broker service which can receive and re-broadcast FRB VOEvents to a list of subscribers. FRB VOEvents that are sent to the FRBCAT broker will also be automatically added to the catalogue (see the FRB VOEvent paper for more information). 

To broadcast a VOEvent you will need a _broker_. We recommend the **Comet broker** which is commonly used for VOEvent communication. To avoid reinventing the wheel, we haven't included any Comet tutorials here, but instead refer you to [the excellent start up guide that already exists](https://comet.readthedocs.io/en/stable/usage/broker.html).

To register as an author with the FRBCAT broker: (information to be added soon re: address, port, IP addresses, etc.)

## Receiving VOEvents from the FRBCAT Broker

Initially, the FRBCAT broker will only receive events from and issue events to subscribed IP addresses from an approved list. To register your broker with the FRBCAT please follow these steps:

(More information to come when the broker is up and running)

## Parsing a VOEvent

VOEvents are easily parsed using the `voeventparse` python package. See [here](http://voevent-parse.readthedocs.io/en/latest/tutorial/index.html) for a full tutorial. 

