import cryptanalib as ca
import feathermodules

padding_menu = """What kind of padding is being used?
1) PKCS#5/PKCS#7
2) ANSI X.923
3) ISO/IEC 7816-4:2005

Please enter a number: """

po_attack_script_skeleton = """# Generated by FeatherDuster
import cryptanalib as ca
import sys

if len(sys.argv) != 2:
   print '[*] Padding oracle attack script'
   print '[*] Usage: %%s <hex-encoded ciphertext or new plaintext>' %% sys.argv[0]
   exit()

def padding_oracle(ciphertext):
   print '''If you are seeing this message, you haven't yet written the padding
      oracle function. Please edit this script to tell it how to interact with
      the oracle.'''
   # HEY! YOU THERE!
   # Here's where you write a function to interact with the padding oracle.
   # This function should invoke the padding oracle with the provided ciphertext
   # and return True for good padding, or False for bad padding.
   # Pseudocode:
   # Send ciphertext to the padding oracle
   # If the padding oracle says the padding is good:
   #   return True
   # Otherwise, if the oracle says the padding is bad:
   #   return False

# To decrypt the first command line argument:
print "The decrypted version of your input is: " + ca.padding_oracle_decrypt(padding_oracle=padding_oracle, ciphertext=sys.argv[1].decode('hex'), block_size=%r, padding_type=%r, iv=%r, verbose=True, hollywood=%r)

# To encrypt the first command line argument:
# print "Your new ciphertext is: " + ca.cbcr(sys.argv[1].decode('hex'), oracle=padding_oracle, is_padding_oracle=True, block_size=%r, verbose=True)
"""

def generate_generic_padding_oracle_attack_script(ciphertexts):
   options = dict(feathermodules.current_options)
   options = prepare_options(options, ciphertexts)
   if options == False:
      print '[*] Options could not be validated. Please try again.'
      return False
   try:
      print '[+] Attempting to write script...'
      fh = open(options['filename'], 'w')
      fh.write(po_attack_script_skeleton % (options['blocksize'],options['padding_type'],options['iv'],options['hollywood'],options['blocksize']))
      fh.close()
   except:
      print '[*] Couldn\'t write to the file with the name provided. Please try again.'
      return False
   print '[+] Done! Your script is available at %s' % options['filename']
   print '[+] The script as-is will not be functional, please edit the padding_oracle() function as described in the generated script.'

def prepare_options(options, ciphertexts):
   if options['blocksize'] == 'auto':
      analysis_results = ca.analyze_ciphertext(ciphertexts)
      if analysis_results['blocksize'] == 0:
         print '[*] Couldn\'t detect a common blocksize.'
         return False
      options['blocksize'] = analysis_results['blocksize']
   else:
      try:
         options['blocksize'] = int(options['blocksize'])
      except:
         print '[*] Blocksize could not be interpreted as a number.'
         return False
   
   # If we actually supported anything but pkcs7, here we would do:
   # arguments['padding_type'] = raw_input(padding_menu)
   # But we don't, so we:
   options['padding_type'] = 'pkcs7'
   
   if options['iv'] == '':
      print '[+] No IV provided, defaulting to null block.'
      options['iv'] = '00'*options['blocksize']
   else:
      try:
         options['iv'].decode('hex')
      except:
         print '[*] IV was not in the correct format. Please provide a hex-encoded IV with length matching the blocksize.'
         return False
      if (len(options['iv'])/2) != options['blocksize']:
         print '[*] IV was not the correct length. Please provide a hex-encoded IV with length matching the blocksize.'
         return False
   
   # We don't use this yet, commented out for now.
   '''
   while True:
      prefix_answer = raw_input('Do you need to use a prefix (no)? ')
      if prefix_answer.lower() not in ['','n','no']:
         prefix = raw_input('Please enter the prefix you want to use, hex encoded: ')
         try:
            arguments['prefix'] = prefix.decode('hex')
            break
         except:
            print '[*] Couldn\'t decode your entry. Is it properly hex encoded?'
            continue
      else:
         arguments['prefix'] = ''
         break
   '''

   options['hollywood'] = (options['hollywood'].lower() not in ['','n','no','no i am lame'])
 
   return options


feathermodules.module_list['padding_oracle'] = {
   'attack_function':generate_generic_padding_oracle_attack_script,
   'type':'block',
   'keywords':['block'],
   'description':'Generate a generic padding oracle attack script skeleton.',
   'options':{
      'filename':'padding_oracle_decrypt.py',
      'hollywood':'no',
      #'padding_type':'pkcs7',
      #'prefix':'',
      'blocksize':'auto',
      'iv':''      
   }
}
