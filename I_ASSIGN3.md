# Assignment 3: "Bare Metal" HTTP Server

This exercise will serve as one component of your final IoT device build coming in a couple of weeks. In this exercise you'll program a *simple* HTTP server in Python using *only* sockets - no frameworks!

To accomplish this, you'll:

* Use the `socket` module to *create a TCP listener that listens on a given port*.
* Accept one TCP connection at a time (no need to worry about threading right now).
* When the connection opens, wait for the client to send an HTTP request.
* Extract key details from the HTTP request: in particular, the verb and path. Also, check for additional data (e.g. in a `POST`) request and extract it as well. Store this data in variables.
* Process the data accordingly. For this exercise you'll create three "routes" as described below.
* Create and form a valid HTTP 1.1 response and send it back to the client. Immediately disconnect the client as soon as the response is finished sending, and return to listening for a connection.

Note that you can implement this on your computer *without needing to use the Pi Pico*. In fact, since we have not as of yet specifically covered Wi-Fi networking code for the Pi Pico, you will want to do this on your laptop.

## Assignment:

1. Write a main loop function that listens for TCP connections on a specific port.

    > While we will use the default port of 80 when we run this code on your Pi Pico, do *not* use port 80 right now. Listening on port 80 requires admin rights to run your program. Instead, choose a port like 5000, 5050, 8001, etc. You can always put the port number in your browser, e.g. `http://localhost:5050`.

2. When a connection arrives, accept the connection (which will create a stream object you can read and write to).
3. From this connection read until you find *two `\r\n` character sequences in a row*. Remember that two `\r\n` sequences indicates the end of the header.
4. Parse the request and header to extract:
    * The verb (`GET`, `POST`, etc.)
    * The path (e.g. `GET /hello`'s path is `/hello`)
    * The headers, as a dictionary

    > **Hint:** Verify the data as well - your program should be robust! Remember that on the first line of an HTTP 1.1 request, the line ends with `HTTP/1.1`. If you ever encounter errors, return a `500` error code and immediately close the connection.
5. Act based upon the *path* of the request. Write at least three *routes* that react to different paths. *Document* your routes in comments in your code.

    > If you're familiar with web development, you understand the concept in play here. A *route* is simply a designation - what should happen when specific paths (or paths that match certain patterns) are requested.
    >
    > For example, you might see a route in a REST API that looks like: `/product/{id:int}`. This would indicate that any time the path `/product/` followed by an integer is requested, run the function connected to that route (and pass in the integer as the parameter `id`).
    >
    > Since we don't have the benefit of frameworks, you don't need to go overboard with this. Don't worry about *parameterized routes* - just write three different routes.
    >
    > Note that one of your routes should simply be the empty route - the `/` route! This should return some kind of renderable page - some simple HTML or even plain text is fine.

6. For two of your three routes, write code that does something minimally dynamic. For example, you could print the current time on one route and print the number of seconds since the app started running in another route. 
7. In each route, construct a return value to return to the client. 
8. Using only a single piece of code (perhaps in a function, but not necessarily required), form the HTTP response as appropriate. I strongly recommend making a function that will produce a fully formed HTTP response ready for sending over the wire. I also recommend including at least two headers: `Content-Length`, which should be the total length of your response **in bytes** (**not** in characters!), and the other should be a content type - typical content types you'll want to consider are `text/plain` (for pure plain text), `text/html` (for HTML data), and `application/json` (for JSON data).
9. Send your HTTP response and then immediately close the connection and wait for another connection.
10. Test your code by accessing the server in your browser by connecting to `localhost`. 

## Samples

Your code should be able to process a request that looks like this:

    GET / HTTP/1.1
    Host: 192.168.34.145:8889
    Connection: keep-alive
    DNT: 1
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
    Accept: text/html,application/xhtml+xml,application/xml; q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
    Accept-Encoding: gzip, deflate
    Accept-Language: en-US,en;q=0.9

This request would be looking to retrieve your `/` route - your default root route.

> [!TIP]
> Browsers can send whichever headers they choose. You need to *consume* and *parse* all the headers, but you can **ignore** headers you don't care about - which in this case is most all of them!

Your code should respond with exactly this type of response:

```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 38

<html><body>Hello World!</body></html>
```

## Hints

* Remember that computers treat characters differently than bytes - especially since Unicode and UTF-8, a single character *does not necessarily equal a single byte*! This is especially important if you use emojis, non-English characters, symbols, etc. In Python, you can use **bytestrings** (example: `b'Hello World'`) to ensure you are dealing with bytes, not non-uniform size characters.
* Write a function that prepares a return response, and have that function accept a paramter which is the entire body (if any) of the response. You can use the byte length of that parameter to determine the value for `Content-Length`. You might also want a parameter for the content type.

## Character Encoding

Modern character encoding schemes like UTF-8 represent individual characters (known as "code points" in Unicode vernacular) as a series of one through four bytes. The actual length of a character depends on a few things:

* If the character falls under pure ASCII, it is still only one byte - this makes UTF-8 backward compatible with ASCII text, in that all valid ASCII text is also valid UTF-8 text.
* Most foreign language characters occupy two bytes - this includes non-Roman scripts like Chinese, Japanese, Arabic, etc.
* Symbols, specialty characters and emojis are typically two, three or four bytes long. Emojis that allow for skin tone encoding usually take up all four bytes. 

In Python, you can convert between arrays of *characters* (varying legnth) to arrays of *bytes* by using the `encode` and `decode` functions. `encode` operates on Unicode strings and *encodes* them to *byte arrays*; `decode` operates on byte arrays and *decodes* them back to characters.

For example:

    unicode_string = "Hello! 😊"
    print(unicode_string) # prints Hello! 😊

    unicode_bytes = unicode_string.encode("utf-8")
    print(unicode_bytes) # prints b'Hello! \xf0\x9f\x98\x8a

    decoded_string = unicode_bytes.decode("utf-8")
    print(decoded_string) # prints Hello! 😊

As you can see, the emoji actually takes up four bytes! 

> [!TIP]
> In practice, in extremely constrained systems, we will simply use the *maximum* length of a character to represent all characters - in this case, even a simple letter `a` would require four bytes to store!

## Sockets

Important tips and tricks for working with sockets.

* Create a socket context: `s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
* Bind the socket for listening: `s.bind(("0.0.0.0", 5050))` (or whichever port you desire)
* Listen for connections: `s.listen(1)` (Allows one connection in the "queue" - if the queue is full, new connections are refused, not held.)
* Accept a connection: `conn = s.accept()`. This blocks until a connection is actually received.
* Now, `conn` can be used like a stream - `write` and `read` operations function just like they do on file objects.
* To close a connection: `conn.close()`

> In these examples, `s` refers to a socket context (which defines the address family - `AF_INET` means "Internet", and the protocol - `SOCK_STREAM` refers to TCP). `conn` refers to an accepted connection that is open; you can read and write from the connection just as if it were a local file on disk.

# Submission

Your submission must include:

* The code for your very simple HTTP server, written in Python.

No screenshots required - I'll be running and reading your code.

## Rules

* **You may NOT use any frameworks**, such as Flask, Django, etc. in this project - you must explicitly use raw socket communications.
* **You MUST properly account for the `\r\n` line endings**. Using `readline()` splits on `\n`, so it will generally still work - you'll just have the `\r` in the string as well.
* **You SHOULD use bytestrings to avoid ambiguity with length of strings**. While it's not strictly required as long as you stick with pure ASCII characters, it's good to account for the possibility of non-English characters, emojis, symbols, etc. 
* Remember that you must submit working, *tested* code - even if your error is obvious, you may lose some credit if you don't go back and fix it!

Submit your work to D2L no later than *Wednesday, November 19th* at 11:59 PM.

## Grading

This assignment is worth **100 points**.

Components:

| Item | Points | Scoring |
|-|-|-|
| Working socket implementation | 30 | Full points if socket connection works properly. Zero points if omitted. Partial loss for uncorrected errors. |
| HTTP Protocol | 30 | Full points if HTTP protocol properly implemented. Loss of points if protocol errors are present. Significant loss if protocol errors prevent any working interaction with a browser. |
| Routes | 40 | Full points for code that parses the path and implements three specific *routes*. 15 point loss per missing route (minimum of 0). |

