
import os
import mutagen.id3
musicroot= '/Users/eki/code/mutagen_script/music/'
tryencodings= ['gb18030', 'cp1252']  # other choices include 'GB2312-80', 'BIG5', 

def find_files_with_ext(path):
    for child in os.listdir(path):
        child= os.path.join(path, child)
        if os.path.isdir(child):
            for mp3 in find_files_with_ext(child):
                yield mp3
        elif child.lower().endswith(u'.mp3'):
            yield child

for path in find_files_with_ext(musicroot):
    print(f'---------------\nTreating file: {path}\n')
    id3= mutagen.id3.ID3(path)
    for key, value in id3.items():
        if not hasattr(value, 'encoding'):
            print('Skipping id3 item due to missing encoding attr:', key)
            # TODO: how many other types of value are there?
            continue
        if value.encoding!=3:
            if value.encoding==0:
                if isinstance(value.text, list):
                    try:
                        bytes= '\n'.join(value.text).encode('iso-8859-1')
                    except TypeError as e:
                        if 'expected str instance, ID3TimeStamp found' in str(e):
                            # TODO: too many different kinds of info avail inside value.text
                            # What are they? How to treat them good?
                            print('ID3TimeStamp found. Skipping ', value.text)
                            continue  
                else:
                    bytes= value.text.encode('iso-8859-1')
                for encoding in tryencodings:
                    try:
                        bytes.decode(encoding)
                        print(f'Succeed with {encoding}')
                    except UnicodeError:
                        pass
                    else:
                        break
                else:
                    raise ValueError(
                'None of the tryencodings work for %r key %r' % (path, key))
                if isinstance(value.text, list):
                    for i in range(len(value.text)):
                        value.text[i]= value.text[i].encode('iso-8859-1').decode(encoding)
                else:
                    value.text = value.text.encode('iso-8859-1').decode(encoding)
            value.encoding= 3
    id3.save()
    print(id3)