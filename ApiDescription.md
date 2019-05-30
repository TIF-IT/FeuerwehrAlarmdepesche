
# Api documentation and usage guid

In this manual we want describe how to use our development.

# Use extenion point

If you would like to extend our functionalit. You can use the extension point system.
Search the code for the function call ModuleRegistry.callExtensionPoints(EXTENSION_TYPE, EXTENSION_OBJECT) and you find the positions where you can extend the code.
If you need more extension points, pleas create a issue and we woul create it in the standard.

Why we use extension points for develop user specific code?
Your idee is that the basic code can be used all the time and can recive updates and fixes without
migration steps. But we would also create a method for the user the extend our development for spezial cases they cant be in standard.

## Add a new module 

  - create a new file for example in modules/email/email_extension_module.py
  - add following lines to it:

        from Alarmdepesche.registry import ModuleRegistry, Api
        @ModuleRegistry.register
        class EmailExtensionModule(Api):
          def config(self):
            ModuleRegistry.registerExtensionPoint("HTML_INTERPRETED", self.interpretHTMLAlarmdepesche)
          def interpretHTMLAlarmdepesche(self, extensionObject):
            (htmlAlarmdepesche, foundAlarmdepesche) = extensionObject
            return (htmlAlarmdepesche, foundAlarmdepesche)

In the code example above you can see the registration of a new module in the modules folder email. The import statement is for the registration as module in our system. The anotation on the class with "@ModuleRegistry.register"is the direct registration for the class and the line "class EmailExtensionModule(Api):" is the new class with the creation as sub class from Api.
The function definition of "config" with the parameter "self" is needed as start point and the "self" is for access to the object.
With the line "ModuleRegistry.registerExtensionPoint("HTML_INTERPRETED",self.interpretHTMLAlarmdepesche)" we regitster our class function interpretHTMLAlarmdepesche als call function for the extension point.

  - Open the __main__.py in the project root and add the import of the new module 

        # Extensions
        from Alarmdepesche.modules.email import sample_email_extension_module

Now oure new module is registerd and where called if the extension point "HTML_INTERPRETED" is called