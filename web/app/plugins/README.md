# Plugins

A plugin is a Python file that serves as an interface between Peaceful Farm and an A/D infrastructure. The repository will be regularly updated with new plugins.

In addition to the provided plugins, users can create their own by writing custom code. This README serves as a comprehensive guide to help you develop your own plugin.

> 💡 **Tips** <br> It is **raccomanded** to start developing your own plugins by using `web/plugins/example.py` as a template.

## Functions  

### **submit_flags**  

The `submit_flags` function is called by the **Peaceful Farm** server to submit flags to the **A/D infrastructure** and earn points.  

#### **Parameters**  
- **flags**: A list of `Flag` class instances. Each instance has several attributes, the most relevant being:  
  - **flag**: The actual flag value.  
  - **status**: The flag's submission status.  
  - **message**: The response message from the infrastructure server.  

#### **Function Structure**  
The function should follow this structure:  

1. Iterate through the list of flags.  
2. Send each flag to the server.  
3. Based on the server’s response:  
   - If accepted, update the flag's status to `ACCEPTED` (a constant from `settings`).  
   - If rejected, update the status to `REJECTED`.  
4. Set the flag's **message** attribute to the server's response.
5. Return a tuple with the following elements:
   - **updated_flags**: A list of `Flag` class instances updated with the new status and messages.
   - **accepted_flags**: The number of flags the server accepted.
   - **rejected_flags**: The number of flags the server rejected.


### targets
The `targets` function is called by the **Peaceful Farm** client to retrive the list of the targets' ip addresses. It must return a list of ip addresses.

### nop
The `nop` function is called by the **Peaceful Farm** client to retrive the nop team's ip. It must return a list with only the nop's ip.

### myteam
The `myteam` function is called by the **Peaceful Farm** client to retrive your team's ip. It must return a list with only the your team's ip.


### **debug**

The `debug` function is called by the **Peaceful Farm** server to simulate the response of the game server. This function acts as an endpoint that must replicate the behavior of the authentic A/D server.  

The `debug` function should be invoked when the constant `FLAGS_SUBMISSION_DEBUG` (defined in `web/app/settings.py`) is set to `True`. To implement this, simply add an `if` statement in the `submit_flags` function to control where the traffic should be routed based on the value of `FLAGS_SUBMISSION_DEBUG`.  

### flagids
The `flagids` function is called by the **Peaceful Farm** client to retrive flagids. It provides a unified interface for clients to interact with the system.
