#See the debuffs
            for debuff in types_json['damage_relations']['double_damage_from']:
                debuff = debuff['name'].capitalize()
                
                #X4 if two types have the same debuff
                if debuff in debuff_list:
                    debuff_list.remove(debuff)
                    debuff_list.append(f'{debuff}X4')
                #Add to the list
                else:
                    debuff_list.append(debuff)
                    
            for buff in types_json['damage_relations']['double_damage_to']:
                buff = buff['name'].capitalize()
                
                #X4 if two types have the same debuff
                if debuff in debuff_list:
                    debuff_list.remove(debuff)
                    debuff_list.append(f'{debuff}X4')
                #Add to the list
                else:
                    debuff_list.append(debuff)