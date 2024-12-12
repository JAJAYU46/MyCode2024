%getDroneCenterFunc
function [I, previousBoxes, previousScores,NowDroneCenter] = getDroneCenterFunc(I, previousBoxes, previousScores, detector) %bboxes, scores)
    fprintf('OK2\n');

    [bboxes, scores] = detect(detector, I, 'Threshold', 1);
    NowDroneCenter = [0, 0];
    % Select strongest detection
    fprintf('OK3\n');

    if ~isempty(scores) &&  ~isempty(bboxes) % Only proceed if scores are not empty        
        [~, idx] = max(scores);    
        %得到center座標然後print
        % Print the bounding box coordinates
        
        %fprintf('Bounding Box: [x: %.2f, y: %.2f, width: %.2f, height: %.2f]\n', ...
        %    bboxes(1), bboxes(2), bboxes(3), bboxes(4));
        
        % Calculate and print the center of the bounding box
        centerX = bboxes(1) + bboxes(3) / 2;
        centerY = bboxes(2) + bboxes(4) / 2;
        fprintf('OK3.5\n');

        % VISUALIZE
        annotation = sprintf('%s, Confidence %4.2f', detector.ModelName, scores(idx));
        
        %i = i + 1;
        NowDroneCenter(1)=centerX;
        NowDroneCenter(2)=centerY;
        I = insertObjectAnnotation(I, 'rectangle', bboxes(idx, :), annotation);
        % Add red point for the center
        I = insertShape(I, 'FilledCircle', [centerX, centerY, 5], 'Color', 'red', 'Opacity', 1);
        fprintf('OK4\n');

        previousScores=scores;
        previousBoxes=bboxes;

    elseif ~isempty(previousScores) %若前一個frame是not empty的話就沿用前一個的
        fprintf('OK5.0\n');

        [~, idx] = max(previousScores);
        fprintf('OK5.1\n');
        centerX = previousBoxes(1) + previousBoxes(3) / 2;
        centerY = previousBoxes(2) + previousBoxes(4) / 2;
        fprintf('OK5.2\n');
        % VISUALIZE
        annotation = sprintf('%s, Confidence %4.2f', detector.ModelName, previousScores(idx));
        fprintf('OK5.3\n');
        NowDroneCenter(1)=centerX;
        NowDroneCenter(2)=centerY;
        %i = i + 1;
        fprintf('OK5.4\n');
        I = insertObjectAnnotation(I, 'rectangle', previousBoxes(idx, :), annotation);
        fprintf('OK5.5\n');
        % Add red point for the center
        I = insertShape(I, 'FilledCircle', [NowDroneCenter(1), NowDroneCenter(2), 5], 'Color', 'red', 'Opacity', 1);
        fprintf('OK5.6\n');
        %<更前> box score如果出框一次是不會繼承，會真的繼承空的
        %previousScores=scores;
        %fprintf('OK5.7\n');
        %previousBoxes=bboxes;
        fprintf('OK5\n');
        %<更後> box 出框或是消失都是繼承之前消失的位置的(所以出框的無人機還能沿著消失前的位置回來)
        %previousScores=previousScores;
        %previousBoxes=previousScores;


        %NowCenter也沿用前一個的
       %<更前> 出框兩次就是出框
    % else %如果前frame和這個frame都是empty的話, 表示無人機真的出框了, 那就回傳center是0,0或是NaN
    % 
    %     
    %     %fprintf('OK6.0\n');
    % 
    %     %NowDroneCenter(1)=0;
    %     %NowDroneCenter(2)=0;
    %     %fprintf('OK6\n');
    % 

    end
end
