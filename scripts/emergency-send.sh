#!/bin/bash

set -o errexit
set -o nounset

usage()
{
    echo "


    Usage:

        # $(basename "${0}") [-]
"
    exit 1
}

while getopts : opt; do
    case "${opt}" in
        \?|*) usage ;;
    esac
done
unset opt

shift $(( OPTIND - 1 ))

if [[ "${#}" != 0 ]]; then
    usage
fi
unset usage

REPO=$(realpath "$(dirname "$(realpath -- "${BASH_SOURCE[0]}")")/..")
cd -- "${REPO}"

./scripts/sms-send.sh "
here's a lady who's sure all that glitters is gold
And she's buying a stairway to heaven.
When she gets there she knows, if the stores are all closed
With a word she cant get what she came for.
Ooh, ooh, and she's buying a stairway to heaven.

There's a sign on the wall but she wants to be sure
'Cause you know sometimes words have two meanings.
In a tree by the brook, there's a songbird who sings,
Sometimes all of our thoughts are misgiven.

Ooh, it makes me wonder,
Ooh, it makes me wonder.

There's a feeling I get when I look to the west,
And my spirit is crying for leaving.
In my thoughts I have seen rings of smoke through the trees,
And the voices of those who stand looking.

Ooh, it makes me wonder,
Ooh, it really makes me wonder.

And it's whispered that soon, if we all call the tune,
Then the piper will lead us to reason.
And a new day will dawn for those who stand long,
And the forests will echo with laughter.

If there's a bustle in your hedgerow, don't be alarmed now,
It's just a spring clean for the May queen.
Yes, there are two paths you can go by, but in the long run
There's still time to change the road you're on.
And it makes me wonder.

Your head is humming and it won't go, in case you don't know,
The piper's calling you to join him,
Dear lady, can you hear the wind blow, and did you know
Your stairway lies on the whispering wind?

And as we wind on down the road
Our shadows taller than our soul.
There walks a lady we all know
Who shines white light and wants to show
How everything still turns to gold.
And if you listen very hard
The tune will come to you at last.
When we all are one and one is all
To be a rock and not to roll.

And she's buying the stairway to heaven.
"

