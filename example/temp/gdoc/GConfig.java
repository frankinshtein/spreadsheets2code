package com.model.gdoc;

/*
 file was automatically generated
*/

import org.jetbrains.annotations.NotNull;
import org.w3c.dom.Node;
import com.google.common.base.MoreObjects;
import java.util.*;

public class GConfig
{
	public static ArrayList<GConfig> items = new ArrayList<>();


    public int indexInArray;


    public void init(Node node, int index, GLoader loader){
    	indexInArray = index;
    }

    public GConfig(){}


    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this)
                .toString();
    }
}