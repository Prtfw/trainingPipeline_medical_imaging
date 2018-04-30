---
typora-copy-images-to: ./images
---

### Analysis:

This notebook contains data visualization and exploration code.

The goal is to explore threshold and other heuristic based methods for cardio lv-segmentation before implementing with machine learning and deep learning options.

Pipeline functions (mostly in .py files) were implemented for imag process and also for feeding into (machine learning / deep learning) model as batches.

- plotted the distribution (position agnostic) of the pixels inside the i-contour vs. pixels between the i-contour and o-countours (muscle)

  ![image-20180429170159543](https://ws2.sinaimg.cn/large/006tKfTcly1fqudojj7cfj309c06aq30.jpg)

- usually there are 2 peaks in plot for the above distributions, since blood pool is darker

    ​	![image-20180429170427014](https://ws4.sinaimg.cn/large/006tKfTcly1fqudonypevj306y06vdfw.jpg)

- check the distribution of the pixel density via 2 sample ks test using a random subset. 
    - this is a non-parametric test of "distance" between the 2 sampling distribution

    - if pvalue is significant, we can reject the hypothesis that the distribusion of pixel densitiy in blood pool (bp) vs heart muscle is the same

    - if pvalue is very small, it gives me more confidence that we can achieve some kind of reasonable segementation based on thresholds

    - wheather the threshold segments are sufficient depends on the business requirement

    - but looking at the distribution histograms we commonly see overlaps which means we don't expect the threshold segmentation to be extremely accurate

      ![image-20180429171529420](/Users/mengningshang/Desktop/Dev_Env/medseg/images/image-20180429171529420.png)

      ![image-20180429171555557](https://ws3.sinaimg.cn/large/006tKfTcly1fqudoojk9zj30eh07gdg3.jpg)

- proceeded to compute a threshold value using one common method "threshold_otsu"
    - use try_all_threshold on a random subset and visually picked the best performing (method) from the try_all_threshold set ('otsu')

        #### one_sample:

        ![image-20180429170916256](https://ws1.sinaimg.cn/large/006tKfTcly1fqudolczd4j30er0hw75h.jpg)

    - computed a blood pool segmentation mask based on the otsu threshold value (only on the region inside the outter contour mask, this region is isolated by calling 'select_region' with the dicom and the o-contour mask, if we do not do this we get a threshold on the whole dicom image (including other organs and structures) instead, which is not what we want)

        #### mask over o-contour (dark ring = Muscle, light interior region = left ventricle blood pool):

        ![image-20180429171315295](https://ws2.sinaimg.cn/large/006tKfTcly1fqudopul23j30c506daa3.jpg)

    - after applying the threshold I compared the IOU (Intersection over Union) score for my own ('otsu') threshold based segmentation vs the gold labeled version
        - custom implemented a IOU_score function that accounts for different sizes in the region, each pixel is identified by it's row, col index

    - also plotted the result of each contour pair with IOU score and ks test pvalues from ('otsu') threshold based segmentation results

        ![image-20180429171354683](https://ws1.sinaimg.cn/large/006tKfTcly1fqudommu2aj30vq0n0tas.jpg)

    - after inspecting the IOU scores, and ks-pvalues for all examples, I conclude threshold only heurisits are unlikely to perform well
        - slightly more than 1/2 (65%) of the dicoms with both i and o contours gave a IOU score of > .75 which is quite low for a medical setting
        - further more the ks-pvalues are also very small (<0.05) in most cases (indicating that the ('otsu') segmentation's pixel density is very different from the gorund truth distribution)

- I would expect low probability of generating high quality segments based on heuristics along

- some other ideas I researched and wanted to test (with the expectation of achieving small improvements are):

    - strech density distribution to imrove contrast inside o-contour
    - canny edge detection inside the o-contour region
    - flood-filling
    - normalizing the images could improve segmentation results (similar to the first idea)
    - try more "dynamic" ways of finding thresholds, (kmean is a clear classical ML technique and Unets is a clear DL option)
      ​