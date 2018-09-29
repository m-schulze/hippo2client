import os
import tempfile
import shutil
import textwrap
import string
import random

from unittest import TestCase

import hippiagent



URL = "http://localhost:8080/"
TIMEOUT = 10


class TestHippiAgent(TestCase):

    def test_is_initiable(self):
        hippiagent.Agent(url=URL, timeout=TIMEOUT)

    def test_major_image(self):
        return
        e = hippiagent.MajorEntity('v1.2.3')
        path_to_image = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph.png")
        e.add_file("graph.png", path_to_image)
        e.add_markdown('001.md', '![graph](graph.png)')
        a = hippiagent.Agent(url=URL, timeout=TIMEOUT)
        a.add(e)
        a.upload()

    def test_major_mass(self):
        return
        for i in range(30):
            id_ = "v{}.{}.{}-{}-g{}".format(
                    random.randint(1, 10), random.randint(1, 10), random.randint(1, 10),
                    random.randint(1, 1000), random.randint(100000, 10000000))
            e = hippiagent.MajorEntity(id_)
            for i in range(10):
                randno = random.randint(1, 1000)
                name = "{}.md".format(randno)
                e.add_markdown(name, '# title')
            a = hippiagent.Agent(url=URL, timeout=TIMEOUT)
            a.add(e)
            a.upload()

    def test_minor_mass(self):
        return
        e = hippiagent.MajorEntity('v1.2.4')
        for i in range(300):
            randno = random.randint(1, 1000)
            name = "{}.md".format(randno)
            e.add_markdown(name, '# title')

        a = hippiagent.Agent(url=URL, timeout=TIMEOUT)
        a.add(e)
        a.upload()

    def test_full_tree(self):
        return
        e = hippiagent.MajorEntity('v1.2.4')
        e.add_markdown('001.md', '[test-001](0001/)')
        e.add_reference('0001', '002.md', 'link to 0001')
        e.minor_add_markdown('0001', '01.md', 'test **passed**')
        path_to_image = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph.png")
        e.minor_add_file('0001', "graph.png", path_to_image)
        e.minor_add_markdown('0001', '02.md', '![graph](graph.png)')

        a = hippiagent.Agent(url=URL, timeout=TIMEOUT)
        a.add(e)
        a.upload()

    def test_full_tree_with_meta(self):
        e = hippiagent.MajorEntity('v1.2.4')

        meta = hippiagent.MetaTest(hippiagent.MetaTest.PASSED)
        e.minor_add_meta('0001', meta)

        e.add_markdown('001.md', '[test-001](0001/)')
        e.add_reference('0001', '002.md', 'link to 0001')
        e.minor_add_markdown('0001', '01.md', 'test **passed**')
        path_to_image = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph.png")
        e.minor_add_file('0001', "graph.png", path_to_image)
        e.minor_add_markdown('0001', '02.md', '![graph](graph.png)')

        a = hippiagent.Agent(url=URL, timeout=TIMEOUT)
        a.add(e)
        a.upload()

    def test_zzz_major_hello_world(self):
        return
        e = hippiagent.MajorEntity('v2.0.0-real-good')
        e.add_markdown('0001.md', '# Real Good Example')

        e.add_markdown('0002.md', '''
        ## Description

        Funky fresh bizzle. Da bomb potenti. Maecenizzle nisl. Its fo rizzle
        elit ante, fizzle my shizz, ullamcorpizzle yo mamma, scelerisque et,
        leo. Crazy egizzle neque. Shit felis. Morbi sure, nisl vitae fringilla
        cursus, libero mi varizzle check it out, sizzle that's the shizzle
        that's the shizzle shut the shizzle up cool dawg. Curabitur consequat
        pizzle its fo rizzle elizzle. Fusce the bizzle dolor funky fresh i'm in
        the shizzle. Go to hizzle ma nizzle, metizzle vel varizzle pot, lorem
        shiznit pharetra dope, eu izzle risus est sizzle est

        - list item 1
        - list item 2
        - list item 3

        ''', detent=True
        )

        path_to_image = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph.png")
        e.add_file("graph.png", path_to_image)
        e.add_markdown('0003.md', '### Illustration\n![graph](graph.png)')

        path_to_image = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rectangle.svg")
        e.add_file("rectangle.svg", path_to_image)
        e.add_markdown('0004.md', '### SVG Illustration\n![graph](rectangle.svg)')

        cmd  = '### Code Block\n'
        cmd += '```\n'
        cmd += '#include<stdio.h>\n'
        cmd += '\n'
        cmd += 'int main() {\n'
        cmd += '    printf("Hello World");\n'
        cmd += '    return 0;\n'
        cmd += '}\n'
        cmd += '```\n'
        e.add_markdown('0005.md', cmd)

        e.add_markdown('0006.md', '''
---
__Advertisement :)__

- __[pica](https://nodeca.github.io/pica/demo/)__ - high quality and fast image
  resize in browser.
- __[babelfish](https://github.com/nodeca/babelfish/)__ - developer friendly
  i18n with plurals support and easy syntax.

You will like those projects!

---

# h1 Heading 8-)
## h2 Heading
### h3 Heading
#### h4 Heading
##### h5 Heading
###### h6 Heading


## Horizontal Rules

___

---

***


## Typographic replacements

Enable typographer option to see result.

(c) (C) (r) (R) (tm) (TM) (p) (P) +-

test.. test... test..... test?..... test!....

!!!!!! ???? ,,  -- ---

"Smartypants, double quotes" and 'single quotes'


## Emphasis

**This is bold text**

__This is bold text__

*This is italic text*

_This is italic text_

~~Strikethrough~~


## Blockquotes


> Blockquotes can also be nested...
>> ...by using additional greater-than signs right next to each other...
> > > ...or with spaces between arrows.


## Lists

Unordered

+ Create a list by starting a line with `+`, `-`, or `*`
+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit
+ Very easy!

Ordered

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa


1. You can use sequential numbers...
1. ...or keep all the numbers as `1.`

Start numbering with offset:

57. foo
1. bar


## Code

Inline `code`

Indented code

    // Some comments
    line 1 of code
    line 2 of code
    line 3 of code


Block code "fences"

```
Sample text here...
```

Syntax highlighting

``` js
var foo = function (bar) {
  return bar++;
};

console.log(foo(5));
```

## Tables

| Option | Description |
| ------ | ----------- |
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |

Right aligned columns

| Option | Description |
| ------:| -----------:|
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |


## Links

[link text](http://dev.nodeca.com)

[link with title](http://nodeca.github.io/pica/demo/ "title text!")

Autoconverted link https://github.com/nodeca/pica (enable linkify to see)


## Images

![Minion](https://octodex.github.com/images/minion.png)
![Stormtroopocat](https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat")

Like links, Images also have a footnote style syntax

![Alt text][id]

With a reference later in the document defining the URL location:

[id]: https://octodex.github.com/images/dojocat.jpg  "The Dojocat"


## Plugins

The killer feature of `markdown-it` is very effective support of
[syntax plugins](https://www.npmjs.org/browse/keyword/markdown-it-plugin).


### [Emojies](https://github.com/markdown-it/markdown-it-emoji)

> Classic markup: :wink: :crush: :cry: :tear: :laughing: :yum:
>
> Shortcuts (emoticons): :-) :-( 8-) ;)

see [how to change output](https://github.com/markdown-it/markdown-it-emoji#change-output) with twemoji.


### [Subscript](https://github.com/markdown-it/markdown-it-sub) / [Superscript](https://github.com/markdown-it/markdown-it-sup)

- 19^th^
- H~2~O


### [\<ins>](https://github.com/markdown-it/markdown-it-ins)

++Inserted text++


### [\<mark>](https://github.com/markdown-it/markdown-it-mark)

==Marked text==


### [Footnotes](https://github.com/markdown-it/markdown-it-footnote)

Footnote 1 link[^first].

Footnote 2 link[^second].

Inline footnote^[Text of inline footnote] definition.

Duplicated footnote reference[^second].

[^first]: Footnote **can have markup**

    and multiple paragraphs.

[^second]: Footnote text.


### [Definition lists](https://github.com/markdown-it/markdown-it-deflist)

Term 1

:   Definition 1
with lazy continuation.

Term 2 with *inline markup*

:   Definition 2

        { some code, part of Definition 2 }

    Third paragraph of definition 2.

_Compact style:_

Term 1
  ~ Definition 1

Term 2
  ~ Definition 2a
  ~ Definition 2b


### [Abbreviations](https://github.com/markdown-it/markdown-it-abbr)

This is HTML abbreviation example.

It converts "HTML", but keep intact partial entries like "xxxHTMLyyy" and so on.

*[HTML]: Hyper Text Markup Language

### [Custom containers](https://github.com/markdown-it/markdown-it-container)

::: warning
*here be dragons*
:::

        ''', detent=True
        )

        a = hippiagent.Agent(url=URL, timeout=TIMEOUT)
        a.add(e)
        a.upload()

