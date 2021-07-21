/****************************************************************************
*
* PROGRAM: demo.c
*
* PURPOSE: Simple application to demonstrate the use of the low level 
*          functions of the OmsMAXkMC DLL (Motion Control DLL) for 
*          communicating with a Pro-Dex / Oregon Micro Systems MAXk motion 
*          controller.  Note see the DLL documentation for higher level 
*          functions that will move the axis and require less application 
*          code. 
*          Link the application with the OmsMAXkMC.lib dll import library.
*
****************************************************************************/
#include <stdio.h>
#include <windows.h>

/* Define  DLL function prototypes & constants */
#include "OmsMAXkMC.H"

#define RECV_LEN 80

void main(void)
{
  HANDLE  hDevice = NULL;
  char    strRecv[RECV_LEN] = {0};
  long    lRetVal = 0;
  
  /* Get a handle to the motor controller device driver */
  hDevice = GetOmsHandle("OmsMAXk1");
  
  if( hDevice == NULL )
  {
    printf("Unable to get a handle to the OmsMAXk1 Driver\n");
    return;
  }

  /* Report device driver version */
  GetOmsDriverVersion( hDevice, strRecv);
  printf("Device Driver:\n  %s\n\n", strRecv);
  
  memset(strRecv, 0, sizeof(char) * RECV_LEN);
  /* Print controller's model */
  lRetVal = SendAndGetString( hDevice, "wy", strRecv);
  if(lRetVal != SUCCESS)
    printf("Error: SendAndGetString returned %d!\n", lRetVal);
  else
    printf("OMS Controller Model:\n  %s\n\n", strRecv);
  
  memset(strRecv, 0, sizeof(char) * RECV_LEN);
  /* Ask the controller for X axis position */
  lRetVal = SendAndGetString( hDevice, "AXRP", strRecv);
  if(lRetVal != SUCCESS)
    printf("Error: SendAndGetString returned %d!\n", lRetVal);
  else
    printf("X axis position before move: %s\n", strRecv);

  /* Move X axis 10000 relative steps */
  lRetVal = MoveOmsAxisRelWait( hDevice, OMS_X_AXIS, 10000, 5000);
  if(lRetVal == MOVE_TIME_OUT)
    printf("Move was not completed within 5 seconds.\n");
  else if(lRetVal != SUCCESS)
    printf("Error: SendAndGetString returned %d!\n", lRetVal);
  
  memset(strRecv, 0, sizeof(char) * RECV_LEN);
  /* Ask the controller for X axis position */
  lRetVal = SendAndGetString( hDevice, "AXRP", strRecv);
  if(lRetVal != SUCCESS)
    printf("Error: SendAndGetString returned %d!\n", lRetVal);
  else
    printf("X axis position after move: %s\n", strRecv);
  
  CloseOmsHandle(hDevice);
}    

