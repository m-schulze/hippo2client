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
        for i in range(10):
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
        e = hippiagent.MajorEntity('v1.2.4')
        for i in range(1000):
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
        """ full features test """
        e = hippiagent.MajorEntity('v2.3.4-fully-featured')


        e.add_markdown('001.md', '# Fully Featured')
        e.add_markdown('002.md', '## Build Times')
        e.add_markdown('003.md', '''
- Compile Duration: 666 seconds
- Test Duration: 1.2 hours
        '''
        )

        e.add_markdown('004.md', '## Unit Tests')

        # unit test 0001
        meta = hippiagent.MetaTest(hippiagent.MetaTest.PASSED)
        e.minor_add_meta('0001', meta)
        e.minor_add_markdown('0001', '01.md', 'cunit test **passed**\n')
        e.minor_add_markdown('0001', '02.md', 'explain probably a little bit more')
        # reference subitem from main page
        e.add_markdown('005.md', '- [unit test 1](0001/)')

        # unit test 0002
        meta = hippiagent.MetaTest(hippiagent.MetaTest.PASSED)
        e.minor_add_meta('0002', meta)
        e.minor_add_markdown('0002', '01.md', 'cunit test **passed**\n')
        e.minor_add_markdown('0002', '02.md', 'explain probably a little bit more')
        # reference subitem from main page
        e.add_markdown('006.md', '- [unit test 2](0002/)')

        # unit test 0003
        meta = hippiagent.MetaTest(hippiagent.MetaTest.FAILED)
        e.minor_add_meta('0003', meta)
        e.minor_add_markdown('0003', '01.md', 'cunit test **failed**\n')
        e.minor_add_markdown('0003', '02.md', 'explain probably a little bit more')
        # reference subitem from main page
        e.add_markdown('007.md', '- [unit test 1](0003/)')

        # unit test 0004
        meta = hippiagent.MetaTest(hippiagent.MetaTest.ERROR)
        e.minor_add_meta('0004', meta)
        e.minor_add_markdown('0004', '01.md', 'cunit test **error**\n')
        e.minor_add_markdown('0004', '02.md', 'explain probably a little bit more')
        # reference subitem from main page
        e.add_markdown('008.md', '- [unit test 1](0004/)\n')

        # e.g. range between 100 and 200 are module tests
        e.add_markdown('100.md', '## Module Tests')

        meta = hippiagent.MetaTest(hippiagent.MetaTest.PASSED)
        e.minor_add_meta('0100', meta)
        e.minor_add_markdown('0100', '01.md', 'cunit test **error**\n')
        e.minor_add_markdown('0100', '02.md', 'explain probably a little bit more')
        # this time with image
        path_to_image = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph.png")
        e.minor_add_markdown('0100', '01.md', '# Module Test 1')
        e.minor_add_file('0100', "graph.png", path_to_image)
        e.minor_add_markdown('0100', '02.md', '![graph](graph.png)')
        # reference subitem from main page
        e.add_markdown('101.md', '- [module test 1](0100/)')

        a = hippiagent.Agent(url=URL, timeout=TIMEOUT)
        a.add(e)
        a.upload()

    def test_zza_tree_with_meta(self):
        return
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
        e.add_markdown('0003.md', '### PNG Illustration\n![graph](graph.png)')

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

# h1 Heading
## h2 Heading
### h3 Heading
#### h4 Heading
##### h5 Heading
###### h6 Heading



## Emphasis

**This is bold text**

__This is bold text__

*This is italic text*

_This is italic text_

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

Don't get it here ... argl

- One Element
- Two elem,ents
    - three
        - Five

Ordered

1. Lorem ipsum dolor sit amet
1. Consectetur adipiscing elit
1. Integer molestie lorem at massa


1. You can use sequential numbers...
1. ...or keep all the numbers as `1.`


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


## Tables

| Option | Description |
|--------|-------------|
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |



### Right aligned columns


| Option | Description |
| ------:| -----------:|
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |


## Links

[link text](http://dev.nodeca.com)

[link with title](http://nodeca.github.io/pica/demo/ "title text!")


        ''', detent=False
        )

        a = hippiagent.Agent(url=URL, timeout=TIMEOUT)
        a.add(e)
        a.upload()

