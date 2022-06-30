# Aurafy

### Video Demo:  

### Description:

The basis of my project is a simple web application that accesses a Spotify user's 'currently playing song' and generates an image that represents the moods of the song, itself. Using the OAuth workflow and the Spotify API application, I generate an access token that enables the user and server to make requests to the API and get info including the user's currently playing song and the song's audio features and analysis data as provided by Spotify.

The landing page is dynamic through the use of Flask Sessions. Since I store the authentication header that I use to make requests to the API in a session variable, I check the existence of this var in order to load links to either the log in page or log-out and 'visualize' pages. Through multiple requests to the API, I get an access token, which lasts 30 minutes, and is required in the API request headers. After authenticating, the server redirects to the 'visualize' page where the functionality of the application is realized. There is a card in the middle of the page which displays the info received from the server. Initially, this card will ask the user to press the refresh button to send a request to the server. When the button is clicked, an AJAX request is sent to the server and the 'analyze' function. Using more API requests, I get audio features like 'valence' and calculate the standard deviation between these features and a predetermined list of means of each feature for the four moods I focus on: energetic, happy, calm, and sad. The lowest stdev is the primary mood and the second lowest is the secondary mood. Using PIL, I randomly generate and image with 'randint' and different color weights. Then, I store this info in a memory buffer and return a dataurl. Ultimately, I send a JSON response to the client with this dataurl alongside other info about the song. If a song isn't currently playing or an ad is playing, according information is shown.

I also created a button in the footer that allows the user to regen an access token using the API's refresh workflow. All in all, the application was a strong test of my ability to implement my ideas into a program. Looking back, there are definite improvements I can make regarding the code, but for such a simple application, they aren't necessarily imperative.

