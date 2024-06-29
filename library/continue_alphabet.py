#!/usr/bin/python

# Copyright: (c) 2024, Jen Giroso (@jgiroso)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
  name: continue_alphabet
  short_description: Find next set alphabetical letters
  version_added: 1.0.0
  author: Jen Giroso (@jgiroso)
  description:
    - From a list of letters find the next and missing letters in alphabetical order.
  options:
    current_letters:
      description: A list of alphabetical letters exactly one letter each.
      type: list
      elements: string
      required: true
    return_number:
      description: 
        - The number of letters to return.
        - If undefined, it will return the rest of the missing alphabet.
      type: int
      required: false

'''

EXAMPLES = r'''
# Return all missing letters of the alphabet
- name: Find all missing letters
  continue_alphabet:
    current_letters: ['a', 'b', 'c']
    # Produces a list of the letters d - z ... ['d', 'e' ... 'y', 'z']

# Find the next specified number of letters
- name: Find three missing letters
  continue_alphabet:
    current_letters: ['a', 'b', 'd']
    return_number: 3
    # Produces the list ['c', 'e', 'f']
'''

RETURN = r'''
  _value:
    description: A list of letters in alphabetical order that were not included in the input.
    type: list
'''

from ansible.module_utils.basic import AnsibleModule
from string import ascii_lowercase

def find_missing_letters(input_letters):
    alphabet = set(ascii_lowercase)
    input_to_lower = set(input_letters.lower())
    missing_letters = sorted(alphabet - input_to_lower)
    return missing_letters

def get_letters():

    module_args = dict(
        current_letters=dict(type='list', required=True),
        return_number=dict(type='int', required=False)
    )

    result = dict(
        changed=False,
        missing_letters=[],
        string_output=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Set input to var and check that all items are a single letter
    input_letters_list= module.params['current_letters']
    single_char_list = all(map(lambda s: len(s) == 1, input_letters_list))
    return_length =  module.params['return_number'] or len(input_letters_list) - 1

    # Validate input list
    if not single_char_list:
        module.fail_json(msg='All input items must be a single letter')

    # Find missing alphabet letters
    letters_string = ''.join(input_letters_list)
    missing_letters = find_missing_letters(letters_string)

    # Return results
    result['missing_letters'] = missing_letters
    result['string_output'] = return_length

    module.exit_json(**result)


def main():
    get_letters()


if __name__ == '__main__':
    main()
