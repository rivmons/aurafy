# Aurafy

### Not intended for use on smaller devices. Please use on a computer/laptop! Also, thanks for checking this out!!!

<img src="https://user-images.githubusercontent.com/103080532/219749782-c39af58f-dc78-41d9-85eb-83088dcfc2e8.gif" width=100% height=30% />

### Description:

The basis of my project is a simple web application that accesses a Spotify user's 'currently playing song' and generates an image that represents the moods of the song, itself. Using the OAuth workflow and the Spotify API application, I generate an access token that enables the user and server to make requests to the API and get info including the user's currently playing song and the song's audio features and analysis data as provided by Spotify.

Using some API requests, I get audio features like 'valence' and calculate the standard deviation between these features and a predetermined list of means of each feature for the four moods I focus on: energetic, happy, calm, and sad. The lowest stdev is the primary mood and the second lowest is the secondary mood. Using PIL, I randomly generate and image with 'randint' and different color weights. Then, I store this info in a memory buffer and return a dataurl. Ultimately, I send a JSON response to the client with this dataurl alongside other info about the song. If a song isn't currently playing or an ad is playing, according information is shown.


## Please note that Spotify only allows API access for authorized users on the Spotify dashboard. Onboarding any user is unavailable as this is more of a hobby project. If you'd like to test this project out, please reach out to me, so I can add you on the list of authorized users :)
