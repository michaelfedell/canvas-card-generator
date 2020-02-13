# Canvas Card Generator

This project takes inspiration from the beautiful artwork and accompanying code released by Luke Patton. Code and art can be found [here](https://canvas-cards.glitch.me/)

To keep these designs fresh and add some uniqueness, this tool takes the original templates, randomizes a style selection and randomizes all the colors used in that particular design.

The javascript for each design has been pulled from [Glitch]() where Luke has shared all his code. These files are included here for convenience in the `canvas` directory

## API

Currently, the tool will simply choose a template and randomize the colors, then return the modified code (javascript) as text which can be rendered by a client browser.

## Frontend

The next phase will extend functionality to actually rendering the canvas card as html and returning this rendered html to the user for direct consumption.

## Other Ideas

Another method for interaction may involve rendering and printing to a png or other image format and returning that file to the user

There may also be a desire to allow the user more control over the randomization of colors - e.g. specifying as "seed color" and then picking complementary colors from random.
