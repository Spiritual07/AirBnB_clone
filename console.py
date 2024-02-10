#!/usr/bin/python3
"""A program that contains the entry point of the command interpreter:"""

import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
import shlex
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class HBNBCommand(cmd.Cmd):
    """Simple command interpreter
        Attributes:
        prompt (str): The command prompt.
    """
    
    prompt = "(hbnb) "

    available_classes = ["BaseModel", "User"]

    def do_EOF(self, args):
        """EOF signal to exit the program."""
        print("")
        return True
    
    def do_quit(self, args):
        """Quit command to exit the program."""
        return True
    
    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def do_create(self, args):
        """Creates a new instance, saves it (to the JSON file) and prints the id
        Usage: create <class_name>
        """
        command = shlex.split(args)
        if len(command) == 0:
            print("** class name missing **")
        elif command[0] not in HBNBCommand.available_classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(f"{command[0]}()")
            storage.save()
            print(new_instance.id)
    
    def do_show(self, args):
        """Prints the string representation of an instance based on the class name and id
        Usage: show <class_name> <id>
        """
        command = shlex.split(args)
        if len(command) == 0:
            print("** class name missing **")
        elif command[0] not in HBNBCommand.available_classes:
            print("** class doesn't exist **")
        elif len(command) == 1:
            print("** instance id missing **")
        else:
            object = storage.all()
            key = "{}.{}".format(command[0], command[1])
            if key in object:
                print(object[key])
            else:
                print("** no instance found **")
    
    def do_destroy(self, args):
        """Deletes an instance based on the class name and id (save the change into the JSON file
        Usage: destroy <class_name> <id>
        """
        command = shlex.split(args)
        if len(command) == 0:
            print("** class name missing **")
        elif command[0] not in HBNBCommand.available_classes:
            print("** class doesn't exist **")
        elif len(command) == 1:
            print("** instance id missing **")
        else:
            object = storage.all()
            key = "{}.{}".format(command[0], command[1])
            if key in object:
                del object[key]
                storage.save()
            else:
                print("** no instance found **")
    
    def do_all(self, args):
        """Prints all string representation of all instances based or not on the class name.
        Usage: all <class_name> or all
        """
        object = storage.all()
        command = shlex.split(args)
        if len(command) == 0:
            for key, value in object.items():
                print(str(value)) 
        elif command[0] not in HBNBCommand.available_classes:
            print("** class doesn't exist **")
        else:
            for key, value in object.items():
                if key.split(".")[0] == command[0]:
                    print(str(value))

    def do_update(slef, args):
        """Updates an instance based on the class name and id by adding or updating
        attribute (save the change into the JSON file).
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        command = shlex.split(args)
        if len(command) == 0:
            print("** class name missing **")
        elif command[0] not in HBNBCommand.available_classes:
            print("** class doesn't exist **")
        elif len(command) == 1:
            print("** instance id missing **")
        else:
            object = storage.all()
            key = "{}.{}".format(command[0], command[1])
            if key not in object:
                print("** no instance found **")
            elif len(command) == 2:
                print("** attribute name missing **")
            elif len(command) == 3:
                print("** value missing **")
            else:
                obj = object[key]
                attribute_name = command[2]
                attribute_value = command[3]
                try:
                    attribute_value = eval(attribute_value)
                except Exception:
                    pass
                setattr(obj, attribute_name, attribute_value)
                obj.save()

if __name__ == "__main__":
    HBNBCommand().cmdloop()