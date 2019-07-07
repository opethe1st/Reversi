## Retrospective
The project is one of my random fun projects that I do to deliberately practise and test the ideas I have come accross.

#### What ideas did I test?
* putting the unittest side by side with the code - I did this and I liked it + using the _test.py suffix so my editor puts the files side by side. The other concern with doing this was that setup.py doesn't let you ignore test files. but I found the way to do it is to use the `python setup.py sdist` command. This actually uses a MANIFEST.in file where you can specify glob patterns for files to include or exlude.
* I tested using circleci and travis - I struggled with both of them till I realized I had gitignored the tox.ini file 😓



#### Lessons
I thought it would be a good idea for the CLI and GUI to share the same interface which they do, but I also realized that I couldn't use the same run function for both because the way of handling events is fundamentally different. For the CLI, it waits for a move to be played, for the GUI, it is event driven with an event loop that polls for events.


#### Improvements
This code has a lot of TODOs (which I kind of abused since some of them are not TODOs but just notes and thoughts i.e annotations) which I am going to ignore for now.
* I could have a view when the game starts when you can select which colour you want your player to be.
* I could written a layer on top of pygame that helps me write cleaner and more succinct code - I found pygame really cumbersome to work with and if I remember correctly it doesn't allow keyword arguments and I didn't get any hightlights when I hovered over the code
The plus to writing the layer would be that my UI won't be devoid of any tests like it is right now. It was definitely harder to work with because I had to manually test and to be honest, I am not convinced it is devoid of bugs 😅.
