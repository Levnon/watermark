import filetype
  
def test(filepath):
 kind = filetype.guess(filepath)
 if kind is None:
  print('Cannot guess file type!')
  
  
 #print('File extension: %s' % kind.extension)
 #print('File MIME type: %s' % kind.mime)
 #print(kind.mime) 
 return kind.mime
if __name__ == '__main__':
     test('cwx.png')
