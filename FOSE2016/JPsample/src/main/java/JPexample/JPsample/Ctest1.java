package JPexample.JPsample;

public class Ctest1 {

    public static void hoge(String a){
        Television tv1 = new Television();
        Television tv2 = new Television();

        tv1.setPlace("居間");
        tv2.setPlace("寝室");

        tv1.setChannel(1);
        tv2.setChannel(8);

        tv1.dispChannel();
        tv2.dispChannel();
    }
}

class Television{
    int channelNo;
    String place;

    Television(){
    	System.out.println("のぶお");
    }

    Television(String name){
    	System.out.println(name);
    }

    
    void setChannel(int newChannelNo){
        channelNo = setChannel2(newChannelNo);
    }

    private int setChannel2(int x){
      return x + 1;
    }

    void setPlace(String newPlace){
        place = newPlace;
    }

    void dispChannel(){
    	// hogehoge.com
        System.out.println(place + "にあるテレビの現在のチャンネルは " + channelNo+ " です");
        /* 
         * sssss
         * aaaa
         */
    }
}
