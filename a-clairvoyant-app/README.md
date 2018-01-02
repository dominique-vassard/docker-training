# Part 2: A claivoyant application

## Goal
We're going to build a very simple application that telles the future given an astrological sign.  
Application will just provides a prediction foir a given astrological sign.

## v0: First version
The application is as simple as it sounds.  
It accepts an argument from command line, read result from a csv fil and print result.  
Test ensures that everything works fine.
  
Test application:  
```
docker run --rm clairvoyant-app:v0 python tests/test_irma_unit.py
docker run --rm clairvoyant-app:v0 python tests/test_irma_integration.py
```
  
Use the application:  
`docker run --rm clairvoyant-app:v0 python app/irma.py aries`
  