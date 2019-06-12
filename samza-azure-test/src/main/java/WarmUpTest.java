import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.RandomAccessFile;
import java.nio.ByteBuffer;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.security.SecureRandom;
import org.junit.Test;


public class WarmUpTest {
  public static void main(String[] args) throws Exception{
    new WarmUpTest().testWriteFilePeriodicly();
  }

  private int FILE_SZIE_BYTES  = 1024 * 1024 * 1024  ;

  private int BUFFER_SIZE = 1024  ;

  private String FILE_NAME_PREFIX = "/Users/fxie/Desktop/";


  private SecureRandom random = new SecureRandom();

  private byte[] buffer = new byte[BUFFER_SIZE];
  @Test
  public void testWriteFilePeriodicly() throws Exception{
    random.nextBytes(buffer);
    File result = new File("result_file");
    result.deleteOnExit();
    result.createNewFile();
    BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(result)));
    for(int i = 0; i < 10; i++){
      String fileName = FILE_NAME_PREFIX + "file-" + i;
      File file = deleteAndCreateNewFile(fileName);
      long time = writeRandomBytesToFile(file, false);
      bw.write(time + "\n");
      //file.deleteOnExit();
      //Thread.currentThread().sleep(60 * 1000);
    }
    bw.flush();
    bw.close();
  }




  private File deleteAndCreateNewFile(String fileName) throws Exception{
    File file = new File(fileName);
    file.deleteOnExit();
    file.createNewFile();
    return file;
  }

  private long writeRandomBytesToFile(File file, boolean isForceToDisk) throws Exception{

    RandomAccessFile raf = new RandomAccessFile(file, "rw");
    FileChannel fc = raf.getChannel();
    MappedByteBuffer mbb = fc.map(FileChannel.MapMode.READ_WRITE, 0, FILE_SZIE_BYTES);
    int t = FILE_SZIE_BYTES / BUFFER_SIZE;
    long start = System.currentTimeMillis();
    for(int i = 0; i < t; i++){

      mbb.put(buffer);
      if(isForceToDisk)
        mbb.force();
    }
    mbb.force();
    long time = (System.currentTimeMillis() - start);
    System.out.println("Write Time : " + time + " millisecond");
    return time;

  }

}
