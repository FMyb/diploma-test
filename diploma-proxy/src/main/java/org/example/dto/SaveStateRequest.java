package org.example.dto;

/**
 * @author Yaroslav Ilin
 */
public class SaveStateRequest {
       private String checkpointName;

       public SaveStateRequest(String checkpointName) {
              this.checkpointName = checkpointName;
       }

       public String getCheckpointName() {
              return checkpointName;
       }

       public void setCheckpointName(String checkpointName) {
              this.checkpointName = checkpointName;
       }
}
