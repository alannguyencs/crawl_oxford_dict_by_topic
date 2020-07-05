import urllib.request
import string


printable = string.printable
dictionary = open("3000words.txt", "w")
exclude = set(string.punctuation)
HOME_URL = "https://www.oxfordlearnersdictionaries.com/"

def clean(s):
    return ''.join(ch for ch in s.lower() if ch not in exclude)

def collect_text(raw_text):
    ans = ""
    post_texts = raw_text.split(">")[1:]
    for post_text in post_texts:
        ans += post_text.split("<")[0]
    return ans

def collect_definition(sub_def):
    print(sub_def)
    tags = ['class=""', 'class="examples"', 'class="collapse"', 'class="prefix"', 'class="dictlink"']
    for tag in tags:
        sub_def = sub_def.split(tag)[0]
    def_word = collect_text(sub_def)
    return def_word

def collect_examples(sub_def):
    tag_1 = '<ul class="examples"'
    tag_2 = '</ul>'
    if tag_1 not in sub_def: return []
    examples = []
    raw_examples = sub_def.split(tag_1)[1].split(tag_2)[0].split('<li')
    for raw_example in raw_examples:
        # print (raw_example)
        raw_example = raw_example.split('</li>')[0]
        example = collect_text(raw_example)
        print ("ex", example)
        examples.append(example)
    return examples

def crawl_page(url_page):

    with urllib.request.urlopen(url_page) as url:
        web_data = url.read().decode('utf-8')
    web_data = ''.join(filter(lambda x: x in printable, web_data))  # delete strange character
    print (web_data)

    keyword = web_data.split("<em>")[1].split("</em>")[0]
    word_type = keyword.split(' ')[-1]
    keyword = keyword.replace(word_type, '')
    dictionary.write(keyword.upper() + '  ' + word_type + "\n\n")

    # print web_data
    # content = web_data.split("jump to other results")[1].split("</div>\n")[0]
    # print content
    definition = web_data.split('class="idioms"')[0].split('class="def')
    for sub_def in definition[2:]:
        # print(sub_def)
        # sub_def = sub_def.replace("class=\"cf\"", "class=\"x")
        # sub_def = sub_def.split('class="x')[0]
        #
        # print (sub_def)
        def_word = collect_definition(sub_def)
        print ("def", def_word)
        if def_word == '': continue
        dictionary.write("def: " + def_word + '\n')

        examples = collect_examples(sub_def)
        for example in examples:
            dictionary.write(example + '\n')
        dictionary.write("\n")
        # print sub_def[0].split("<")[0].split(">")[-1]
        # def_word = sub_def[0].split("<")[0].split(">")[-1]
        # if len(def_word) < 3:
        #     break
    #     dictionary.write("def: " + def_word+ "\n")
    #     for ss in sub_def[1:]:
    #         line = ""
    #         for block in ss.split("<")[:-1]:
    #             line += block.split(">")[-1]
    #         if ". " or ".\n" in line:
    #             line = line.split('.')[0]
    #         # print line
    #         dictionary.write("ex: " + line+ "\n")
    #     # print
    #     dictionary.write("\n")
    #
    dictionary.write("-" * 15 + "\n\n")



# crawl_page("https://www.oxfordlearnersdictionaries.com/definition/english/christian")

def get_difficulty_level(raw_word):
    difficulty_levels = ['a1', 'a2', 'b1', 'b2', 'c1', 'c2']
    for level in difficulty_levels:
        if '\"' + level + '\"' in raw_word:
            return level

def get_href(raw_word):
    return raw_word.split('<a href=\"')[1].split('\"')[0]

def crawl_topic_page(url_page):
    with urllib.request.urlopen(url_page) as url:
        web_data = url.read().decode('utf-8')
    web_data = ''.join(filter(lambda x: x in printable, web_data))  # delete strange character

    # print (web_data)
    raw_words = web_data.split("<li id=\"l2")[1:]
    raw_words = [raw_word.split("li>")[0] for raw_word in raw_words]
    for raw_word in raw_words:
        keyword = raw_word.split('data-hw=\"')[1].split('\"')[0]
        difficulty_level = get_difficulty_level(raw_word)
        href = get_href(raw_word)
        if difficulty_level in ['b1', 'b2']:
            print(keyword, difficulty_level, href)
            crawl_page(HOME_URL + href)


crawl_topic_page("https://www.oxfordlearnersdictionaries.com/topic/religion-and-festivals")

