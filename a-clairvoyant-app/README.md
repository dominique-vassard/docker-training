# Part 2: A claivoyant application

## 0. Goal
We're going to build a very simple application that telles the future given an astrological sign.  
Application will just provides a prediction foir a given astrological sign.

## 1: First version
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
  
## 2. Clairvoyant Web API
### 2.1 Configure and start the server

### 2.2. A better access to code  

## 3. What about changing python version?

## 4. Add a real database
### 4.1. Getting mysql to work
### 4.2. Use mysql from code
### 4.3. The right way to connect containers  

## 5. The data problem

## 6. One application, one command